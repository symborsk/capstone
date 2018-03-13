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
    public partial class ChangeOptionsPage : ContentPage
    {
        public AppOptions options { get; set; }

        public ChangeOptionsPage()
        {
            InitializeComponent();

            options = new AppOptions();
            BindingContext = this;
        }

        async void Save_Clicked(object sender, EventArgs e)
        {
            //When the user clicks save we use the messaging service to post an update call
            //Keeps this process async and smooth
            MessagingCenter.Send(this, "UpdateOptions", options);
            //Async return to root page
            await Navigation.PopToRootAsync();
        }

         private void UpdateOptions_Clicked(object sender, EventArgs e)
        {

        }
       
    }
}
