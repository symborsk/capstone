using System;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;

namespace AIHubMobile
{
	[XamlCompilation(XamlCompilationOptions.Compile)]
	public partial class AIDetailsPage : ContentPage
	{
        WeatherStationDetailViewModel viewModel;

        //We need this default constructor by definition
        public AIDetailsPage()
        {
            viewModel = new WeatherStationDetailViewModel();
            BindingContext = viewModel;
            Title = "AI Page";
            InitializeComponent();
        }

        //When the page is connected we simply bind the proper view model class
        //This View model will represent a list item in detail
        public AIDetailsPage(WeatherStationDetailViewModel passedInViewModel)
        {
            InitializeComponent();
            DetailWeatherSets.ItemsSource = passedInViewModel.RgSets;
            BindingContext = this.viewModel = passedInViewModel;

            Title = "AI Info Station: " + viewModel.Item.StationName;
            //Change the selected index
            this.dateDropDown.SelectedIndex = 0;
        }

        async void Config_Clicked(object sender, EventArgs e)
        {
            await Navigation.PushAsync(new DeviceConfigPage(viewModel.Item.statOptions, viewModel.Item.StationName));
        }

        private void Picker_SelectedIndexChanged(object sender, EventArgs e)
        {
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
            await Navigation.PushModalAsync(new AboutPage(), false);
        }

    }
}