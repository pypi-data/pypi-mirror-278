import os
import click
from subprocess import Popen
import time
import multiprocessing
import shutil
import webbrowser

cwd = os.getcwd()


@click.command()
@click.argument(
    "command", required=True, type=click.Choice(["init", "configure", "dev", "prod"])
)
def main(command: str) -> None:
    # import these here to avoid error when user is configuring (`pinnacle configure`)
    from pinnacle_cli.constants import (
        HOST,
        PORT,
        PYTHON_PORT,
        OPENAPI_PORT,
        DIRECTORY,
    )

    if command == "dev" or command == "prod":
        from pinnacle_cli.py.dev_scheduler import run_scheduled
        # import these here to avoid error when user is configuring (`pinnacle configure`)
        from pinnacle_cli.constants import (
            HOST,
            PORT,
            PYTHON_PORT,
            DIRECTORY,
            OPENAPI_PORT,
        )

        pinnacle_dir = os.path.join(cwd, DIRECTORY)
        if not os.path.exists(pinnacle_dir):
            should_create_dir = input(
                f"Directory {pinnacle_dir} does not exist. Press enter to create it at {pinnacle_dir} (y/n): "
            )
            if should_create_dir.lower() == "y":
                os.makedirs(pinnacle_dir, exist_ok=True)
            else:
                click.echo("Cannot proceed without the directory. Exiting.")
                return

        if command == "dev":
            click.echo("Running in development mode")

            metadata_dir = os.path.join(cwd, DIRECTORY, ".metadata")
            os.makedirs(metadata_dir, exist_ok=True)

            py_endpoints_file = os.path.join(metadata_dir, "py_endpoints.json")
            if os.path.exists(py_endpoints_file):
                os.remove(py_endpoints_file)

            server_logs_path = os.path.join(metadata_dir, "server.log")
            if os.path.exists(server_logs_path):
                os.remove(server_logs_path)

            server_logs_fd = open(server_logs_path, "a+")
            os.environ["PINNACLE_CWD"] = cwd
            python_server = Popen(
                [
                    "uvicorn",
                    "pinnacle_cli.py.dev_server:app",
                    "--host",
                    HOST,
                    "--port",
                    str(PYTHON_PORT),
                    "--reload",
                ],
                stderr=server_logs_fd,
            )

            # Import these before running the scheduled process
            from pinnacle_cli.py.dev_scheduler import run_scheduled

            scheduled_process = multiprocessing.Process(target=run_scheduled)
            scheduled_process.start()

            while not os.path.exists(py_endpoints_file):
                time.sleep(0.5)

            openapi_server = Popen(
                [
                    "uvicorn",
                    "pinnacle_cli.openapi.app:app",
                    "--host",
                    HOST,
                    "--port",
                    str(OPENAPI_PORT),
                    "--reload",
                ],
                stderr=server_logs_fd,
            )

            reverse_proxy_server = Popen(
                [
                    "mitmdump",
                    "--listen-host",
                    HOST,
                    "-p",
                    str(PORT),
                    "-s",
                    f"{os.path.dirname(os.path.abspath(__file__))}/proxy/main.py",
                ],
                env=os.environ,
                cwd=os.path.join(os.path.dirname(os.path.abspath(__file__)), "proxy"),
            )

            time.sleep(0.5)

            tail_logs = Popen(
                ["tail", "-F", "-n", "+15", server_logs_path]
            )  # This skips the outputs that display the Python and OpenAPI port numbers

            try:
                full_host = "http://" + HOST + ":" + str(PORT)
                print(f"Opening API endpoint docs {full_host}/pinnacle/api_docs ...")
                webbrowser.open(f"{full_host}/pinnacle/api_docs")
                reverse_proxy_server.wait()
            except Exception as e:
                click.echo(f"Error running Python dev server: {e}")
            finally:
                print("Terminating servers")
                reverse_proxy_server.terminate()
                python_server.terminate()
                openapi_server.terminate()
                scheduled_process.terminate()
                tail_logs.terminate()
                server_logs_fd.close()

    if command == "configure" or command == "init":
        from pinnacle_cli.utils import write_or_update_pinnacle_env
        is_init = command == "init"
        click.echo(f"Running in {"initialization" if is_init else "configuration" } mode")
        user_host = (
            input(f"Enter the value for PINNACLE_HOST (current: {HOST}): ") or HOST
        )
        write_or_update_pinnacle_env("PINNACLE_HOST", user_host)
        try:
            user_port = (
                int(input(f"Enter the value for PINNACLE_PORT (current: {PORT}): "))
                or PORT
            )
        except ValueError:
            user_port = 8000

        if not (0 <= user_port <= 65535):
            raise ValueError(
                "The provided port number is outside the valid range (0-65535)."
            )

        write_or_update_pinnacle_env("PINNACLE_PORT", str(user_port))
        user_dir = (
            input(f"Enter the value for PINNACLE_DIRECTORY (current: {DIRECTORY}): ")
            or DIRECTORY
        )
        write_or_update_pinnacle_env("PINNACLE_DIRECTORY", user_dir)

        if is_init:
            user_abs_dir =os.path.join(cwd, user_dir)
            os.makedirs(user_abs_dir, exist_ok=True)
            cli_dir = os.path.dirname(os.path.abspath(__file__))
            shutil.copyfile(
                os.path.join(cli_dir, "examples/hello_world.py"),
                os.path.join(user_abs_dir, "hello_world.py")
            )


        click.echo(
            f" {"Initialization" if is_init else "Configuration" } complete. Run `pinnacle dev` to start the development server."
        )

       


if __name__ == "__main__":
    main()
