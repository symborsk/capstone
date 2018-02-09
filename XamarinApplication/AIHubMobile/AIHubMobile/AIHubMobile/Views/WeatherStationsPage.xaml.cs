/**
 * WeatherStationsPage.xaml.cs
 * By: John Symborski
 * Capstone Group 2
 * This file is the back end functionality bound to the Weather Item Page Markup. It will perform any logic and
 * events the page has
 * */

using System;
using System.Collections.Generic;
using System.Threading.Tasks;

using Xamarin.Forms;

namespace AIHubMobile
{
    public partial class WeatherStationsPage : ContentPage
    {
        WeatherStationsViewModel viewModel;

        public WeatherStationsPage()
        {
            InitializeComponent();

            BindingContext = viewModel = new WeatherStationsViewModel();
        }

        async void OnItemSelected(object sender, SelectedItemChangedEventArgs args)
        {
            var item = args.SelectedItem as WeatherStation;
            if (item == null)
                return;

            //Async loading of the deatil page
            await Navigation.PushAsync(new WeatherItemDetailPage(new WeatherStationDetailViewModel(item)));

            // Manually deselect item
            ItemsListView.SelectedItem = null;
        }

        async void AddItem_Clicked(object sender, EventArgs e)
        {
            await Navigation.PushAsync(new ChangeOptionsPage());
        }

        protected override void OnAppearing()
        {
            base.OnAppearing();

            if (viewModel.Items.Count == 0)
                viewModel.LoadItemsCommand.Execute(null);
        }
    }
}