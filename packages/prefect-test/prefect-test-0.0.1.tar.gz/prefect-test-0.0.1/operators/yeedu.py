from urllib.parse import urlparse
from prefect.variables import Variable
from prefect.blocks.system import Secret
from hooks.yeedu import YeeduHook

class YeeduPrefectJobRunOperator():

    def __init__(self, job_url_name, username,password, *args, **kwargs):
        
        super().__init__(*args, **kwargs,)
        self.var_url = job_url_name
        self.var_username = username
        self.var_password = password
        self.username = self.get_username()
        self.password = self.get_password()
        self.job_url = self.get_url()
        self.hook: YeeduHook = YeeduHook(conf_id=self.conf_id, tenant_id=self.tenant_id, base_url=self.base_url, workspace_id=self.workspace_id, connection_id=self.connection_id)

   
    def extract_ids(self):
        url = self.get_url()       
        parsed_url = urlparse(url)
        path_segments = parsed_url.path.split('/')
        tenant_id = path_segments[2] if len(path_segments) > 2 else None
        workspace_id = path_segments[4] if len(path_segments) > 4 else None

        if 'notebook' in path_segments:
            conf_id = path_segments[path_segments.index('notebook') + 1] if len(path_segments) > path_segments.index('notebook') + 1 else None
            job_type = 'notebook'
        elif 'conf' in path_segments:
            conf_id = path_segments[path_segments.index('conf') + 1] if len(path_segments) > path_segments.index('conf') + 1 else None
            job_type = 'conf'
        else:
            conf_id = None
            job_type = None
            
        # Extract base URL and append :8080
        base_url = f"{parsed_url.scheme}://{parsed_url.hostname}:8080/api/v1/"

        return base_url, tenant_id, int(workspace_id), job_type, int(conf_id)

         
    def get_url(self):

        job_url_json = Variable.get(self.var_url)
        job_url = job_url_json.value
        print(job_url)
        return job_url

    def get_password(self):
        secret_block = Secret.load(self.var_password)
        password = secret_block.get()
        print(password)
        return password

    def get_username(self):
        username = Variable.get(self.var_username)
        print(username.value)
        return username.value
