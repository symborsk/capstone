/**
 * WeatherItemDetailViewModel.cs
 * By: John Symborski
 * Capstone Group 2
 * Defines the interactions between the views and the model of the weather detail item. This simply defines the item that will 
 * bind to the view when a user dills into an item.
 * */
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Threading.Tasks;
using Xamarin.Forms;

namespace AIHubMobile
{
    public class WeatherStationDetailViewModel : BaseViewModel
    {
        public WeatherStation Item { get; set; }
        private ObservableCollection<WeatherSet> _rgSets;
        public RangeObservableCollection<WeatherSet> RgSets {get; set;}
        public WeatherSet.WeatherSetDateRanges dateRange;
        public Command RefreshWeatherSets { get; set; }

        public WeatherStationDetailViewModel(WeatherStation item = null)
        {
            Title = "Weather Details: " + item?.StationName;
            dateRange = WeatherSet.WeatherSetDateRanges.Today;
            Item = item;

            RgSets = new RangeObservableCollection<WeatherSet>();
            _rgSets = new ObservableCollection<WeatherSet>();
            RefreshWeatherSets = new Command(async () => await LoadObservableCollection());          
        }

        public async Task LoadObservableCollection()
        {

            IsBusy = true;

            bool succ = await WeatherStationDependency.RefreshWeatherSets(WeatherSet.WeatherSetDateRanges.AllTime);
            IEnumerable<WeatherStation> items = await WeatherStationDependency.GetAllWeatherSets(true);
            _rgSets.Clear();
            foreach (var item in items)
            {
                if(item.StationName == Item.StationName)
                {
                    Item.rgWeatherSets.Clear();
                    foreach(var weatherSet in item.rgWeatherSets)
                    {
                        Item.rgWeatherSets.Add(weatherSet);
                    }
                }
            }

            await Task.Run(()  =>
            {
                DateTime upperbound = DateTime.Now;
                DateTime lowerbound;

                try
                {
                   

                    switch (dateRange)
                    {
                        case WeatherSet.WeatherSetDateRanges.Today:
                            lowerbound = upperbound.Date;
                            break;
                        case WeatherSet.WeatherSetDateRanges.PastThreeDays:
                            lowerbound = upperbound.Date.AddDays(-3);
                            break;
                        case WeatherSet.WeatherSetDateRanges.PastWeek:
                            lowerbound = upperbound.Date.AddDays(-7);
                            break;
                        case WeatherSet.WeatherSetDateRanges.ThisMonth:
                            lowerbound = new DateTime(upperbound.Year, upperbound.Month, 1);
                            break;
                        case WeatherSet.WeatherSetDateRanges.ThisYear:
                            lowerbound = new DateTime(upperbound.Year, 1, 1);
                            break;
                        default:
                            lowerbound = DateTime.MinValue;
                            break;
                    }

                    _rgSets.Clear();
                    foreach (WeatherSet weatherItem in Item.rgWeatherSets)
                    {
                        if (weatherItem.RecordedTime <= upperbound.AddMinutes(1) && weatherItem.RecordedTime >= lowerbound)
                        {
                            _rgSets.Add(weatherItem);
                        }
                    }

                    RgSets.ClearAndAddRange(_rgSets);

                }
                catch (Exception ex)
                {
                    Console.WriteLine("Exception during loading station data: " + ex.Message);
                }
                finally
                {
                    IsBusy = false;
                }
            });                  
        }
    }
}
