import cassandra
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

cloud_config= {
        'secure_connect_bundle': 'secure-connect-database1.zip' ## Current path (jupyter)
}
auth_provider = PlainTextAuthProvider('nlbFMayuZbErPZwWalbFNoIl', 'xdCOgAMczejL28JoOwRXkktd1vUTF63ryh8p57-POoWOtM6dZ+OAWZ,FwLz-vTgbhGvAMe+_HajGg623evv1AC1Xc8j,st-SZQee8PUXM-I_i6Mj,T2ZsT2xqK2sU5-_')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

row = session.execute("select release_version from system.local").one()
if row:
    print(row[0])
else:
    print("An error occurred.")

row=session.execute("SELECT * FROM system_schema.keyspaces;")
for i in row:
    print(i[0])

row = session.execute("CREATE KEYSPACE keyS1 WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 3};")