CREATE ROLE [DatabaseRole_Admin]
    AUTHORIZATION [dbo];


GO
ALTER ROLE [DatabaseRole_Admin] ADD MEMBER [admin];

