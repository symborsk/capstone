
/*
WeatherSet.sql
John Symborski
Capstone Group 2

This is the T-sql script to initialize the SQL Database
*/
CREATE TABLE [dbo].[WeatherSet] (
    [StationId]    BIGINT   NOT NULL,
    [RecordedTime] DATETIME CONSTRAINT [DF_WeatherSet_RecordedTime] DEFAULT (getutcdate()) NOT NULL,
    [Temperature]  INT      NULL,
    [Humidity]     INT      NULL,
    [Visibility]   INT      NULL,
    [Acceleration] INT      NULL,
    CONSTRAINT [PK_WeatherSet] PRIMARY KEY CLUSTERED ([RecordedTime] ASC)
);

