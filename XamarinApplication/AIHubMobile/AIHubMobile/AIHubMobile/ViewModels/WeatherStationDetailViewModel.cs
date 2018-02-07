/**
 * WeatherItemDetailViewModel.cs
 * By: John Symborski
 * Capstone Group 2
 * Defines the interactions between the views and the model of the weather detail item. This simply defines the item that will 
 * bind to the view when a user dills into an item.
 * */
using System;
using System.Collections.ObjectModel;
using System.Threading.Tasks;
using Xamarin.Forms;

namespace AIHubMobile
{
    public class WeatherStationDetailViewModel : BaseViewModel
    {
        public WeatherStation Item { get; set; }
        public ObservableCollection<WeatherSet> rgSets;

        public WeatherStationDetailViewModel(WeatherStation item = null)
        {
            Title = "Station Name: " + item?.stationId;
            Item = item;

            rgSets = new ObservableCollection<WeatherSet>();
            //Create the observable collection for binding to list view
            foreach (WeatherSet weatherItem in item.rgWeatherSets)
            {
                rgSets.Add(weatherItem);
            }

        }

        //Async load of the items
        async Task ExecuteLoadItemsCommand()
        {
            return;
        }

        async void OnItemSelected(object sender, SelectedItemChangedEventArgs args)
        {
            var item = args.SelectedItem as WeatherSet;
            if (item == null)
                return;

        }


    }
}
