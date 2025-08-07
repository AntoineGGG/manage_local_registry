import subprocess
import sys
import os
from dotenv import load_dotenv

load_dotenv()


class ImageManager:
    def __init__(self):
        self.local_image_repository = os.getenv("local_image_repository")
        self.local_repository = os.getenv("local_registry")
        os.environ["HTTPS_PROXY"] = os.getenv("https_proxy")
        os.environ["NO_PROXY"] = os.getenv("NO_PROXY")

    def pull_tag_push_image(self):
        try:
            # Ask the user for the image to pull
            artifact = input("Enter the image to pull (e.g., quay.io/thanos/thanos:v1.03): ")

            repository = '/'.join(artifact.split("/")[1:])

            print(f"Split repository {'/'.join(repository)}")

            # Pull the image
            pull_command = ["podman", "pull", artifact]
            subprocess.run(pull_command, check=True)
            print(f"Successfully pulled {artifact}")

            # Get the image ID
            inspect_command = ["podman", "inspect", artifact, "--format", "{{.Id}}"]
            image_id = subprocess.check_output(inspect_command, text=True).strip()
            print(f"Image ID: {image_id}")

            # Tag the image
            tag_command = ["podman", "tag", image_id, f"{self.local_image_repository}{repository}"]
            subprocess.run(tag_command, check=True)
            print(f"Successfully tagged {image_id} as {self.local_image_repository}{repository}")

            # Push the image to the local registry
            push_command = ["podman", "push", f"{self.local_image_repository}{repository}"]
            subprocess.run(push_command, check=True)
            print(f"Successfully pushed {self.local_image_repository}{repository}")

        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
            sys.exit(1)



if __name__ == "__main__":
    imageManager = ImageManager()
    imageManager.pull_tag_push_image()
