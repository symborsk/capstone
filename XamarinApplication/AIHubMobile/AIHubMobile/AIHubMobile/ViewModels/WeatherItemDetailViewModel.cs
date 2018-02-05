/**
 * WeatherItemDetailViewModel.cs
 * By: John Symborski
 * Capstone Group 2
 * Defines the interactions between the views and the model of the weather detail item. This simply defines the item that will 
 * bind to the view when a user dills into an item.
 * */
using System;

namespace AIHubMobile
{
    public class WeatherItemDetailViewModel : BaseViewModel
    {
        public WeatherSet Item { get; set; }
        public WeatherItemDetailViewModel(WeatherSet item = null)
        {
            Title = "Station Name: " + item?.StationId;
            Item = item;
        }
    }
}
