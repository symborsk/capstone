/**
 * MainPage.cs
 * By: John Symborski
 * Capstone Group 2
 * This file initializes the main tabbed style pages we want to use for this app
 * it initializes the main displays differently for different Runtime Platforms.
 * */

using System;

using Xamarin.Forms;

namespace AIHubMobile
{
    public class MainPage : TabbedPage
    {
        //Initialize the main page with it tabs
        public MainPage()
        {
            Page itemsPage, aboutPage = null;

            switch (Device.RuntimePlatform)
            {
                case Device.iOS:
                    itemsPage = new NavigationPage(new WeatherStationsPage())
                    {
                        Title = "View Weather"
                    };

                    aboutPage = new NavigationPage(new AboutPage())
                    {
                        Title = "About"
                    };
                    itemsPage.Icon = "tab_feed.png";
                    aboutPage.Icon = "tab_about.png";
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
