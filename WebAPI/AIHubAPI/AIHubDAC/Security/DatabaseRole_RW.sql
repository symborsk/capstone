CREATE ROLE [DatabaseRole_RW]
    AUTHORIZATION [dbo];


GO
ALTER ROLE [DatabaseRole_RW] ADD MEMBER [Sql-Server-RW];

