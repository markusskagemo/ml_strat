#property copyright " "
#property link      "github.com/saturdayquant"
#property version   "1.00"

input const int save_mod = 60;

string SUBFOLDER = "Research/ml_tickdata";
int filehandle;
//+------------------------------------------------------------------+
int OnInit() {
    string FILENAME = "\\" + TimeToStr(TimeCurrent(), TIME_DATE) + ".csv";
    filehandle = FileOpen(SUBFOLDER + FILENAME, FILE_READ|FILE_WRITE|FILE_CSV); 
    return(INIT_SUCCEEDED);
}
void OnDeinit(const int reason) {
    FileClose(filehandle);
}
//+------------------------------------------------------------------+
void OnTick() {
    if(TimeCurrent() % save_mod == 0) {
        //Considering mean shift will only calibrate daily, the rest of the data will be discarded and therefore YYYY-MM-DD becomes superfluous. 
        string dt_str = TimeToStr(TimeCurrent(), TIME_DATE|TIME_SECONDS);
        string to_csv = /*dt_str + "," + */Bid;  
        if(filehandle != INVALID_HANDLE) {
            FileSeek(filehandle, 0, SEEK_END); 
            FileWrite(filehandle, to_csv);
            FileFlush(filehandle);
        }
    }
}