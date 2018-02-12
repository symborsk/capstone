CREATE ROLE [DatabaseRole_RO]
    AUTHORIZATION [dbo];


GO
ALTER ROLE [DatabaseRole_RO] ADD MEMBER [Sql-Server-RO];

