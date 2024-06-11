import oci


class OCIUtils:
    def __init__(self, config_file_path="~/.oci/config", passphrase=None):
        if not config_file_path:
            raise ValueError("config_file_path is required")

        config = oci.config.from_file(config_file_path)
        if passphrase:
            config["pass_phrase"] = passphrase

        self.client = oci.object_storage.ObjectStorageClient(config)

    def upload_file(self, namespace: str, bucket_name: str, file_path: str):
        with open(file_path, "rb") as file:
            object_name = file_path.split("/")[-1]
            self.client.put_object(namespace, bucket_name, object_name, file)
        return f"File {object_name} uploaded to bucket {bucket_name}"
