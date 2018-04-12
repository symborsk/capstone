/**
 * AboutViewModel.cs
 * By: John Symborski
 * Capstone Group 2
 * Defines the interactions between the views and the model of the about module. Simply give us any commands we need within 
 * the markup.
 * */

using System;
using System.Windows.Input;

using Xamarin.Forms;

namespace AIHubMobile
{
    public class AboutViewModel : BaseViewModel
    {
        public AboutViewModel()
        {
            Title = "About";

            //This will be replaced with our web portal once it is made
            OpenWebCommand = new Command(() => Device.OpenUri(new Uri("http://174.3.172.24/")));
        }

        public ICommand OpenWebCommand { get; }
    }
}