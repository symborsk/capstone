/**
 * BaseViewModel.cs
 * By: John Symborski
 * Capstone Group 2
 *   Our Base functionality view model. Define any shared behaviour between all the view models.
 * */

using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using Xamarin.Forms;

namespace AIHubMobile
{
    public class BaseViewModel : INotifyPropertyChanged
    {
        //Define the factory dependeny service for getting the weather sets
        public IRestClient<WeatherStation> WeatherStationDependency => DependencyService.Get<IRestClient<WeatherStation>>() ?? new RestClient();

        bool isBusy = false;
        public bool IsBusy
        {
            get { return isBusy; }
            set {
                SetProperty(ref isBusy, value);
                OnPropertyChanged("IsBusy");
            }
        }

        string title = string.Empty;
        public string Title
        {
            get { return title; }
            set { SetProperty(ref title, value); }
        }

        protected bool SetProperty<T>(ref T backingStore, T value,
            [CallerMemberName]string propertyName = "",
            Action onChanged = null)
        {
            if (EqualityComparer<T>.Default.Equals(backingStore, value))
                return false;

            backingStore = value;
            onChanged?.Invoke();
            OnPropertyChanged(propertyName);
            return true;
        }

        #region INotifyPropertyChanged
        public event PropertyChangedEventHandler PropertyChanged;
        protected void OnPropertyChanged([CallerMemberName] string propertyName = "")
        {
            var changed = PropertyChanged;
            if (changed == null)
                return;

            changed.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
        #endregion
    }
}
