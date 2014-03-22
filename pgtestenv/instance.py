# -*- coding: utf-8

import sys
import os
import pickle
import shutil
import commands

class PgInstance(object):
	def __init__(self, path, clean_on_delete=False):
		self.config = {
		'path':os.path.abspath(path),
		'port':None
		}

		self.clean_on_delete = clean_on_delete

		try:
			self.load_conf()
		except IOError,e:
			pass

	def __del__(self):
		if self.clean_on_delete:
			try:
				self.stop()
				self.clean()
			except:
				pass
			print("Cleaning up %s..."%(self))

	def __unicode__(self):
		return u"<PgInstance path='%s' port='%s'>"%(self.config['path'], self.config['port'])

	def __str__(self):
		return "<PgInstance path='%s' port='%s'>"%(self.config['path'], self.config['port'])

	def run_command(self, cmd, expected_status=0):
		print ">>>> %s"%(cmd)
		status,output = commands.getstatusoutput(cmd)
		if status != expected_status:
			raise RuntimeError("Command '%s' failed!"%(cmd))
		return output

	def load_conf(self):
		# try to open the file
		config = pickle.load( open(os.path.join(self.config['path'],'config.pickle')) )
		pg_version = open( os.path.join(self.config['path'], 'PG_VERSION')).read().strip()
		self.config['version'] = pg_version

		self.config.update(config)

	def info(self):
		"""Returns a string of information about this instance"""
		self.is_initialized(True)

		ret = "\n".join(["%s = %s"%(k,v) for k,v in self.config.items()])
		ret += "\nrunning = %s"%(self.is_running())

		return ret

	def is_running(self):
		self.is_initialized(True)
		# Find the socket file
		sockfile = ".s.PGSQL.%s"%(self.config['port'])
		if not os.path.exists( os.path.join(self.config['path'], sockfile)):
			return False
		return True

	def is_initialized(self, throw_exception=False):
		try:
			self.load_conf()
		except IOError,e:
			print e
			if throw_exception:
				raise RuntimeError("ERROR: Directory '%s' is not initialized"%(self.config['path']))
			return False
		return True
		#return os.path.exists(os.path.join(self.config['path'],'config.pickle'))

	def initdb(self, version, port, encoding="UTF-8", locale="en_US.UTF-8", superuser="postgres"):
		# Write config file for ourselves
		config = {
			#'path':self.path,
			'version':version,
			'port':port,
			'encoding':encoding,
			'locale':locale,
			'superuser':superuser,
		}
		self.config.update(config)

		if self.is_initialized() or os.path.exists(self.config['path']):
			raise RuntimeError("ERROR: Cannot initdb, directory '%s' already exists"%(self.config['path']))
		
		cmd = '/usr/lib/postgresql/%s/bin/pg_ctl -D %s initdb -o "--encoding=%s --locale=%s -U %s"'%(self.config['version'], self.config['path'], self.config['encoding'], self.config['locale'], self.config['superuser'])
		self.run_command(cmd)

		conf_fp = open(os.path.join(self.config['path'],'config.pickle'),'w')
		conf_fp.write(pickle.dumps(self.config))

	def start(self, port=None):
		self.is_initialized(True)

		if port:
			self.config['port'] = port
		cmd = '/usr/lib/postgresql/%s/bin/pg_ctl -w -D %s -l %s/postgresql.log start -o "-k %s --port=%s"'%(self.config['version'], self.config['path'], self.config['path'], self.config['path'], self.config['port'])
		print self.run_command(cmd)

	def stop(self):
		self.is_initialized(True)
		cmd = '/usr/lib/postgresql/%s/bin/pg_ctl -D %s stop -m fast'%(self.config['version'], self.config['path'])
		print self.run_command(cmd)

	def clean(self, confirm=False):
		if self.is_running():
			raise RuntimeError("ERROR: The server is still running, not deleting anything.")
		print "Removing directory '%s'"%(self.config['path'])
		datadir = self.config['path']
		really_delete = False
		if not confirm:
			really_delete = True
		elif confirm and raw_input("Really delete the directory '%s'? (Y/N) "%(datadir)) == 'y':
			really_delete = True
		if really_delete:
			shutil.rmtree(datadir)

	def connect(self, *args, **kwargs):
		import psycopg2
		if not kwargs.has_key('user'):
			kwargs['user'] = self.config['user']
		kwargs['host'] = self.config['path']
		if not kwargs.has_key('port'):
			kwargs['port'] = self.config['port']
		return psycopg2.connect(*args, **kwargs)

	def test_connection(self, *args, **kwargs):
		conn = self.connect(*args, **kwargs)
		cur = conn.cursor()
		cur.execute('select version();')
		return cur.fetchall()