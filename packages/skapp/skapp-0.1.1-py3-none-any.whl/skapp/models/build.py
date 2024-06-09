import subprocess
import tempfile
from typing import Optional
from pydantic import BaseModel

# import docker
from python_on_whales import docker


class ImageBuild(BaseModel):
    prefix: str = "docker.io"
    push: bool = True
    pull: bool = False
    name: str
    context: str = "./"
    dockerfile: str = "Dockerfile"
    tag: Optional[str] = None
    image: Optional[str] = None
    platforms: list[str] = []
    target: Optional[str] = None
    md5version: Optional[list[str]] = []
    dependencies: Optional[list[str]] = []


    def get_md5version(self):
        import hashlib

        m = hashlib.md5()

        content = []
        for verfile in self.md5version:
            with open(verfile, "r") as f:
                content.append(f.read())

        m.update("".join(content).encode("utf-8"))
        return m.hexdigest()


    def build(self, client: "docker.DockerClient", image_version: str, deps: list["ImageBuild"] = []) -> str:
        # Use docker-py to build the image
        separator = ":" if ":" not in self.prefix else "-"

        if self.md5version:
            image_version = self.get_md5version()

        self.tag = f"{self.prefix}{separator}{self.name}-{image_version}"

        exists = False
        if self.md5version:
            try:
                client.images.pull(self.tag)
            except:
                pass
            else:
                exists = True


        if exists:
            print(f"Image {self.tag} already exists")
        else:
            print(f"Building {self.name} as {self.tag} with dockerfile {self.dockerfile} in {self.context}")

            dockerfile_path = self.dockerfile
            if self.dependencies:
                # Generate tempfile
                dockerfile_path = tempfile.mktemp()

                with open(self.dockerfile, "r") as f:
                    content = f.read()
                    print(deps, self.dependencies)
                    content = content.format(**{dep.name: dep.tag for dep in deps})
                    with open(dockerfile_path, "w") as f:
                        f.write(content)


            docker_command = [
                "docker",
                "buildx",
                "build",
                "--platform",
                ",".join(self.platforms or ["linux/arm64"]),
                "-t",
                self.tag,
                self.context,
                "-f",
                dockerfile_path,
                "--push" if self.push else "--load",
            ]

            if self.target is not None:
                docker_command.extend(["--target", self.target])

            print(" ".join(docker_command))
            process = subprocess.Popen(
                docker_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )

            # Stream and print the output
            for line in process.stdout:
                print(line, end="")

        # # return tag
        # # Wait for the command to finish
        # # process.wait()

        # # config = docker.buildx.bake(targets=self.platforms or ['linux/amd64'], load=True, push=self.push)

        # # breakpoint()

        # image = client.images.get(tag)

        # # image, logs = client.images.build(
        # #     path=self.context,
        # #     dockerfile=self.dockerfile,
        # #     tag=tag,
        # #     platform="linux/amd64",
        # # )
        # # for log in logs:
        # #     print(log)

        # # if self.push:
        # #     for pushlog in client.images.push(tag, stream=True):
        # #         print(pushlog)

        # self.tag = tag
        # self.image = image

    @classmethod
    def new(cls, **config) -> "ImageBuild":
        return cls(**config)


class Builds(list[ImageBuild]):
    item_class = ImageBuild
