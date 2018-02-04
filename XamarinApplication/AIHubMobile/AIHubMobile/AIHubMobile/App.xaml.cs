﻿using System;

using Xamarin.Forms;

namespace AIHubMobile
{
    public partial class App : Application
    {
        public App()
        {
            InitializeComponent();

            if (Device.RuntimePlatform == Device.iOS)
                MainPage = new MainPage();
            else
            {
                MainPage = new NavigationPage(new MainPage());  
            }
                
        }
    }
}