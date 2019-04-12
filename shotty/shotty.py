import boto3
import botocore
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def filter_instances(project):
	instances = []
	
	if project:
		filters = [{'Name':'tag:Project', 'Values':[project]}]
		instances = ec2.instances.filter(Filters=filters)
	else:
		instances = ec2.instances.all()
	
	return instances 


@click.group()
def cli():
	"""shotty manages snapshots"""


@cli.group('volumes')
def volumes():
	"""Commands for volumes"""
@volumes.command('list')
@click.option('--project', default=None, help="Only instances for project(tag Project: <name>)")	
def list_volumes(project):
	"Volumes List"
	instances = filter_instances(project)
	
	for i in instances:
		for v in i.volumes.all():
			print(
			
			v.id,
			i.id,
			v.state,
			str(v.size)+"GiB",
			v.encrypted and 'Encrypted' or 'Not Encrypted'			
			)
			
			return
		return













@cli.group('instances')
def instances():
	"""Commands for instances"""
	
	
	
@instances.command('snapshots')
@click.option('--project', default=None, help="Only instances for project(tag Project: <name>)")
def snapshots_instances(project):
	"Instance snapshots"
	instances = filter_instances(project)
	
	for i in instances:
		i.stop()
		print("Stopping the instance{0}".format(i.id))
		i.wait_until_stopped()
		for v in i.volumes.all():
			v.create_snapshot(Description="Created my Automation")
		print("Starting")
		i.start()  
		i.wait_until_running()
	return
			



	
@instances.command('list')
@click.option('--project', default=None, help="Only instances for project(tag Project: <name>)")	
def list_instances(project):
	"Ec2 List"
	instances = filter_instances(project)
		  
	for i in instances:	
		tags =  {t['Key']:t['Value'] for t in i.tags or []}
		print(
			i.id,
			i.instance_type,
			i.key_name,
			i.launch_time,
			i.placement['AvailabilityZone'],
			i.state['Name'],
			i.public_dns_name,
			tags.get('Project','<no project>')
			) 
			
	return 
@instances.command('stop')
@click.option('--project', default=None, help="Only instances for project(tag Project: <name>)")	
def stop_instances(project):
	"Stop Instance"
	instances = filter_instances(project)
	
	for i in instances:
		print('Stopping the instances')
		try:
			i.stop()
		except botocore.exceptions.ClientError:
			print("Could not stop the instance:{}".format(i.id))
			continue

@instances.command('start')
@click.option('--project', default=None, help="Only instances for project(tag Project: <name>)")	
def start_instances(project):		
	"Starting Instance"
	instances = filter_instances(project)
		
	for i in instances:
		print('Starting the instance={}'.format(i.id))
		try:
			i.start()
		except botocore.exceptions.ClientError:
			print("Could not start the instance:{}".format(i.id))
			continue

if __name__=='__main__':
	cli()
	 