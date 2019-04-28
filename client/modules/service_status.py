# external
import logging, json, time, subprocess, select, threading, re
# internal
import core

@core.add_action("update_status")
def send_status(data, client):
	core.socket_send(client, json.dumps({
		"action":"receive_status"
	}))

if core.config.client.check_ssh:
	f = subprocess.Popen(['tail','-F',"/var/log/auth.log"],\
	        stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	p = select.poll()
	p.register(f.stdout)

	def check_ssh_auth_logs():
		#Apr 27 16:28:45 <hostname> sshd[4125]: Accepted <method> for <user> from <ip> port <port> ssh2
		ssh_accept_regex = "\w*\s\d*\s\d*:\d*:\d*\s(\S*)\ssshd\[\d*\]:\sAccepted\s(\w*)\sfor\s(\w*)\sfrom\s(\S*)\sport\s(\d*)\sssh2"
		# match output ('<hostname>', '<method>', '<user>', '<ip>', '<port>') [0] -> [4] (1) -> (5)
		while True:
		    if p.poll(1):
		        #print(f.stdout.readline().decode("utf-8"))
		        accept_search = re.search(ssh_accept_regex, f.stdout.readline().decode("utf-8"))
		        if accept_search is not None:
		        	packet = {
		        		"action":"ssh_login",
		        		"hostname":accept_search.group(1),
		        		"method":accept_search.group(2),
		        		"user":accept_search.group(3),
		        		"ip":accept_search.group(4),
		        		"port":accept_search.group(5)
		        	}
		        	logging.info(f"Connection as \"{packet['user']}@{packet['hostname']}\" from \"{packet['ip']}:{packet['port']}\".")
		        	core.socket_send(core.client, json.dumps(packet))
		        	continue
		    time.sleep(1)

	logging.info("Enabled SSH logs checker.")
	authThread = threading.Thread(name="SSH Logger",target=check_ssh_auth_logs)
	authThread.daemon = True
	core.threads.append(authThread)
else:
	logging.info("SSH logs checker not enabled.")