from Scripts.s7 import client


def RayoCRN_Test(DbName,Start,Size):
    try:
        value = client.Client.db_read(DbName,Start,Size)
        return (1, value)
    except Exception as ex:
        return (0, str(ex))