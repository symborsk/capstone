CREATE TABLE [dbo].[WeatherSet] (
    [StationId]    BIGINT   NOT NULL,
    [RecordedTime] DATETIME CONSTRAINT [DF_WeatherSet_RecordedTime] DEFAULT (getutcdate()) NOT NULL,
    [Temperature]  INT      NULL,
    [Humidity]     INT      NULL,
    [Visibility]   INT      NULL,
    [Acceleration] INT      NULL,
    CONSTRAINT [PK_WeatherSet] PRIMARY KEY CLUSTERED ([RecordedTime] ASC)
);

