### Usage:

### Requirements
* Ansible version >= 2.8
* New resource group in Azure

### Steps
1. Clone GitHub repository:
```bash
git clone https://github.com/pim-zwiers/Sentia-Assessment-1.git
```
2. Navigate to ARM templates in repository:
```bash
cd Sentia-Assessment-1/Deployments/ARM-Templates
```
3. Edit parameters in azuredeploy.parameter.json
4. Deploy ARM template to Azure
```powershell 
New-AzResourceGroupDeployment -ResourceGroupName "<resource-group-name>" -TemplateFile .\azuredeploy.json -TemplateParameterFile .\azuredeploy.parameter.json
```
5. Navigate to ansible in repository:
```bash
cd ../ansible
```
6. Edit the resource group under "include_vm_resource_groups:" in **myazure_rm.yml** to your resource group
7. Create Ansible environment variables to store Azure Credentials:
```bash
export AZURE_SUBSCRIPTION_ID=<your-subscription_id>
export AZURE_CLIENT_ID=<security-principal-appid>
export AZURE_SECRET=<security-principal-password>
export AZURE_TENANT=<security-principal-tenant>
```
8. Go to Azure portal and get the newly created Data Lake Gen2's Storage Account Key and Storage Account Name.
9. Export to environment variables:
```bash
export STORAGE_ACCOUNT_NAME=<storage-account-name>
export STORAGE_ACCOUNT_KEY=<storage-account-key>
```
10. Make sure the hosts are reachable (if the username set earlier is different to your machine's add ``--user <username>`` to the command):
```bash
ansible all -m ping -i ./myazure_rm.yml
```
11. Run playbook against hosts (if the username set earlier is different to your machine's add ``--user <username>`` to the command):
```bash
ansible-playbook -i myazure_rm.yml playbook.yml
```
12. Open a browser and navigate to the Load Balancer's Public IP, you should be able to see the website now

## Link to documentation
- [Documentation](./Documentation/README.md).