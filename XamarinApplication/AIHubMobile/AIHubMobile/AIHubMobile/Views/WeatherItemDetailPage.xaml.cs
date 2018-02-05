/**
 * WeatherItemsDetailPage.xaml.cs
 * By: John Symborski
 * Capstone Group 2
 * This file is the back end functionality bound to the Weather Detail Page Markup. It will perform any logic and
 * events the page has
 * */

using System;

using Xamarin.Forms;

namespace AIHubMobile
{
    public partial class WeatherItemDetailPage : ContentPage
    {
        WeatherItemDetailViewModel viewModel;

        //We need this default constructor by definition
        public WeatherItemDetailPage()
        {
            InitializeComponent();

            var item = new WeatherSet(1, Convert.ToDateTime("1995-01-04"), 10, 60, 8, 10);
            viewModel = new WeatherItemDetailViewModel(item);
            BindingContext = viewModel;
        }

        //When the page is connected we simply bind the proper view model class
        //This View model will represent a list item in detail
        public WeatherItemDetailPage(WeatherItemDetailViewModel viewModel)
        {
            InitializeComponent();

            BindingContext = this.viewModel = viewModel;
        }
    }
}
