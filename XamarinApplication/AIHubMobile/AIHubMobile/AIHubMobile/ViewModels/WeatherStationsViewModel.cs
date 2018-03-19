/**
 * WeatherItemViewModel.cs
 * By: John Symborski
 * Capstone Group 2
 * Defines the interactions between the views and the model of the weather set item. Also subscribes any messaging services
 * the xamarin application may need to run.
 * */

using System;
using System.Collections.ObjectModel;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading.Tasks;
using Xamarin.Forms;

namespace AIHubMobile
{
    public class WeatherStationsViewModel : BaseViewModel
    {
        //Collection that can be viewed
        public ObservableCollection<WeatherStation> WeatherStations { get; set; }
        public Command LoadItemsCommand { get; set; }

        public WeatherStationsViewModel()
        {
            Title = "View Weather";
            WeatherStations = new ObservableCollection<WeatherStation>();
            LoadItemsCommand = new Command(async () => await ExecuteLoadItemsCommand());

            //WHen update the config options calls the service
            MessagingCenter.Subscribe<DeviceConfigPage, StationOptions>(this, "UpdateOptions", async (obj, option) =>
            {
                await WeatherStationDependency.UpdateStationOptions(option);
            });
        }

        //Async load of the items
        async Task ExecuteLoadItemsCommand()
        {
            if (IsBusy)
                return;

            IsBusy = true;

            try
            {
                WeatherStations.Clear();
                //From the main page we want to always show them all the data
                bool succ = await WeatherStationDependency.RefreshWeatherSets(WeatherSet.WeatherSetDateRanges.AllTime);
                IEnumerable<WeatherStation> items = await WeatherStationDependency.GetAllWeatherSets(true);
                
                foreach (var item in items)
                {
                    WeatherStations.Add(item);
                }
            }
            catch (Exception ex)
            {
                Debug.WriteLine(ex);
            }
            finally
            {
                IsBusy = false;
            }
        }
    }
}
