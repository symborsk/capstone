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

        public WeatherItemDetailPage(WeatherItemDetailViewModel viewModel)
        {
            InitializeComponent();

            BindingContext = this.viewModel = viewModel;
        }
    }
}
