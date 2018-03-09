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

namespace AIHubMobile
{
    public partial class WeatherItemDetailPage : ContentPage
    {
        WeatherStationDetailViewModel viewModel;
        //ObservableCollection<WeatherSet> sets;
        //We need this default constructor by definition
        public WeatherItemDetailPage()
        {
            InitializeComponent();
            viewModel = new WeatherStationDetailViewModel();
            BindingContext = viewModel;
        }

        //When the page is connected we simply bind the proper view model class
        //This View model will represent a list item in detail
        public WeatherItemDetailPage(WeatherStationDetailViewModel viewModel)
        {
            InitializeComponent();
            WeatherSetListView.ItemsSource = viewModel.rgSets;
            BindingContext = this.viewModel = viewModel;
        }

        async void Config_Clicked(object sender, EventArgs e)
        {
            await Navigation.PushAsync(new ChangeOptionsPage());
        }

        private void Picker_SelectedIndexChanged(object sender, EventArgs e)
        {

        }
    }
}
