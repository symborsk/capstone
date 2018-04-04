using System;
using System.Collections.Generic;
using System.Text;

namespace AIHubMobile
{
    public class StationOptions
    {
        public EditableStationOptions editOptions { set; get; }
        public ReadOnlyStationOptions readOnlyOptions { set; get; }

        public StationOptions(EditableStationOptions editOpt, ReadOnlyStationOptions readOnly)
        {
            editOptions = editOpt;
            readOnlyOptions = readOnly;
        }
    }
}
