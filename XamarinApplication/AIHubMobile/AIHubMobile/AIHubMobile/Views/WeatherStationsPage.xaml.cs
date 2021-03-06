﻿/**
 * WeatherStationsPage.xaml.cs
 * By: John Symborski
 * Capstone Group 2
 * This file is the back end functionality bound to the Weather Item Page Markup. It will perform any logic and
 * events the page has
 * */

using Xamarin.Forms.Xaml;
using Xamarin.Forms;

namespace AIHubMobile
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class WeatherStationsPage : ContentPage
    {
        WeatherStationsViewModel weatherStationViewModel;

        public WeatherStationsPage()
        {
            InitializeComponent();

            BindingContext = weatherStationViewModel = new WeatherStationsViewModel();
        }

        async void OnItemSelected(object sender, SelectedItemChangedEventArgs args)
        {
            var item = args.SelectedItem as WeatherStation;
            if (item == null)
                return;

            //Async loading of the deail page        
            await Navigation.PushAsync(new WeatherStationDetailPage(new WeatherStationDetailViewModel(item)));
            
            // Manually deselect item
            ItemsListView.SelectedItem = null;
        }

        protected override void OnAppearing()
        {
            base.OnAppearing();

            if (weatherStationViewModel.WeatherStations.Count == 0)
                weatherStationViewModel.LoadItemsCommand.Execute(null);
        }
    }
}