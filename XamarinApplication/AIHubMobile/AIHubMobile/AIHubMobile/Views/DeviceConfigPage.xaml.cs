/**
 * ChangeOptions.xaml.cs
 * By: John Symborski
 * Capstone Group 2
 * This file is the back end functionality bound to the Weather Item Page Markup. It will perform any logic and
 * events the page has
 * */

using System;
using System.Collections.Generic;
using Xamarin.Forms.Xaml;
using Xamarin.Forms;

namespace AIHubMobile
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class DeviceConfigPage : ContentPage
    {
        public StationOptions stationOption { get; set; }
        public string deviceName { get; set; }

        public DeviceConfigPage(StationOptions options, string devName)
        {
            InitializeComponent();
            BindingContext = stationOption = options; 
            deviceName = devName;         
        }

         private async void UpdateOptions_Clicked(object sender, EventArgs e)
        {
            MessagingCenter.Send(this, "UpdateOptions", new Tuple<string, StationOptions>(deviceName, stationOption));
            
            await Navigation.PopAsync(); ;
        }
       
    }
}
