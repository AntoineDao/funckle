from pathlib import Path
import io
import os
from typing import Tuple
import tarfile
import gzip
import typer
import shutil
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from pydantic import BaseModel
from .settings import settings

transport = AIOHTTPTransport(
    url=f'{settings.funckle_server}graphql',
    headers={
        'authorization': 'Bearer ' + settings.speckle_auth_token,
    }
)
# Select your transport with a defined url endpoint
# Or transport = RequestsHTTPTransport(url='YOUR_URL')
# Or transport = HTTPXTransport(url='YOUR_URL')
# Or transport = HTTPXAsyncTransport(url='YOUR_URL')

client = Client(transport=transport)

query = gql('''
mutation UploadPackage($name: String!, $description: String, $readme: String, $sourceLocation: String, $version: String!, $file: Upload!) {
  uploadPackage(
    name: $name
    description: $description
    readme: $readme
    sourceLocation: $sourceLocation
    version: $version
    file: $file
  ) {
    functionVersion {
      id
      version
      function {
        id
      }
    }
  }
}
''')
            
class DeployConfig(BaseModel):
    name: str
    description: str
    sourceLocation: str


def create_tar_gz_file(folder_path: Path, version: str) -> Tuple[str, Path]:
    # Create a filename for the compressed tarfile
    build_dir = folder_path.joinpath(".build")

    # Create the .build directory if it doesn't exist
    os.makedirs(build_dir, exist_ok=True)
    #  remove zip file if it exists
    # if filename.exists():
    #     shutil.rmtree(filename)
    return shutil.make_archive(folder_path.joinpath(".build").joinpath(version), 'gztar', folder_path), build_dir

def deploy_package(folder_path: Path, version: str):
    deploy_config_path = folder_path.joinpath(".funckle.json")
    if not deploy_config_path.exists():
        raise Exception("No .funckle.json file found in the specified folder")
    deploy_config = DeployConfig.model_validate_json(deploy_config_path.read_text())
    readme = folder_path.joinpath("README.md").read_text()

    file, build_dir = create_tar_gz_file(folder_path, version)

    params = deploy_config.model_dump()
    params["version"] = version
    params["readme"] = readme
    try:
        with open(file, "rb") as f:

            params["file"] = f

            result = client.execute(
                query, variable_values=params, upload_files=True
            )
            typer.echo("Function deployed successfully")

            function_id = result["uploadPackage"]["functionVersion"]["function"]["id"]
            function_version_id = result["uploadPackage"]["functionVersion"]["id"]
            typer.echo('Success!')
            typer.echo(f'Check out your function at: {settings.funckle_server}functions/{function_id}/{function_version_id}')
    except Exception as e:
        typer.echo("Error deploying function")
        typer.echo(e)
    finally:
        shutil.rmtree(build_dir)
