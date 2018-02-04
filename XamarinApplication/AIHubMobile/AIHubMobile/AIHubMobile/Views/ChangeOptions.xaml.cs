using System;
using System.Collections.Generic;

using Xamarin.Forms;

namespace AIHubMobile
{
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
            MessagingCenter.Send(this, "UpdateOptions", options);
            await Navigation.PopToRootAsync();
        }

        private void UpdateOptions_Clicked(object sender, EventArgs e)
        {
            //TODO: Update Options functionality
        }
    }
}
