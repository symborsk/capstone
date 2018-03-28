using System;

using Xamarin.Forms;

namespace AIHubMobile
{
    public class DetailTabbedPage : TabbedPage
    {
        //We need the viewmodel to establish a page
        public DetailTabbedPage(WeatherStationDetailViewModel viewModel)
        {
            Page itemsPage, aboutPage = null;

            switch (Device.RuntimePlatform)
            {
                case Device.iOS:
                    itemsPage = new NavigationPage(new WeatherStationDetailPage(viewModel))
                    {
                        Title = "View Weather"
                    };

                    aboutPage = new NavigationPage(new AboutPage())
                    {
                        Title = "About"
                    };
                    itemsPage.Icon = "tab_feed.png";
                    aboutPage.Icon = "pcl.png";
                    break;
                default:
                    itemsPage = new WeatherStationsPage()
                    {
                        Title = "View Weather"
                    };

                    aboutPage = new AboutPage()
                    {
                        Title = "About"
                    };
                    break;
            }

            Children.Add(itemsPage);
            Children.Add(aboutPage);

            Title = Children[0].Title;
        }

        //Update the title when the page is changed
        protected override void OnCurrentPageChanged()
        {
            base.OnCurrentPageChanged();
            Title = CurrentPage?.Title ?? string.Empty;
        }
}
}
