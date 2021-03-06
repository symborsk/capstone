﻿/**
 * WeatherItemsDetailPage.xaml.cs
 * By: John Symborski
 * Capstone Group 2
 * This file is the back end functionality bound to the Weather Detail Page Markup. It will perform any logic and
 * events the page has
 * */

using System;
using System.Collections.ObjectModel;
using Xamarin.Forms;
using System.Threading.Tasks;
using Xamarin.Forms.Xaml;

namespace AIHubMobile
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class WeatherStationDetailPage : ContentPage
    {
        WeatherStationDetailViewModel viewModel;

        //We need this default constructor by definition
        public WeatherStationDetailPage()
        {
            InitializeComponent();
            viewModel = new WeatherStationDetailViewModel();
            BindingContext = viewModel;   
        }

        //When the page is connected we simply bind the proper view model class
        //This View model will represent a list item in detail
        public WeatherStationDetailPage(WeatherStationDetailViewModel passedInViewModel)
        {
            InitializeComponent();
            DetailWeatherSets.ItemsSource = passedInViewModel.RgSets;
            BindingContext = this.viewModel = passedInViewModel;
            
            //Change the selected index
            dateDropDown.SelectedIndex = 0;
        }

        async void Config_Clicked(object sender, EventArgs e)
        {
            StationOptions opt = await viewModel.GetStationOptions();
            await Navigation.PushAsync(new DeviceConfigPage(opt, viewModel.Item.StationName));
        }

        private void Picker_SelectedIndexChanged(object sender, EventArgs e)
        {
            //TODO: Update Options functionality
            Picker pick = (Picker)sender;

            String selected = pick.SelectedItem.ToString();
            WeatherSet.WeatherSetDateRanges range;
            switch (selected)
            {
                case "Today":
                    range = WeatherSet.WeatherSetDateRanges.Today;
                    break;
                case "Past 3 Days":
                    range = WeatherSet.WeatherSetDateRanges.PastThreeDays;
                    break;
                case "Past Week":
                    range = WeatherSet.WeatherSetDateRanges.PastWeek;
                    break;
                case "This Month":
                    range = WeatherSet.WeatherSetDateRanges.ThisMonth;
                    break;
                case "This Year":
                    range = WeatherSet.WeatherSetDateRanges.ThisYear;
                    break;
                default:
                    range = WeatherSet.WeatherSetDateRanges.AllTime;
                    break;
            }
            viewModel.dateRange = range;

            //Refresh the weather sets
            if (DetailWeatherSets != null)
            { 
                viewModel.RefreshWeatherSets.Execute(null);
            }   
        }

        private async void ViewAIInfo(object sender, EventArgs e)
        {
            await Navigation.PushAsync(new AIDetailsPage(viewModel), false);
        }


    }
}
