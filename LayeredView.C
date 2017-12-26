
#include <iostream>
#include <fstream>
#include <dirent.h>
#include <regex>
//namespace {
std::regex isLayered("\\b([0-9]+)layered.csv",std::regex::ECMAScript);
std::regex element("\\b([0-9]+),([0-9]+),([0-9]+)\\s*",std::regex::ECMAScript);
//}
constexpr int TOTAL_TICKTIME = 25;
constexpr int CRASHED_EPNS = 11;

struct TimeFrameLossTickTimeEPNRatio {
    //std::vector< std::pair< std::vector<int> , std::vector<int>>> data;
    int data[TOTAL_TICKTIME / 5][CRASHED_EPNS];
    private:
   
    void loadFile(const std::string& filename){
        std::smatch res;
        std::regex_search(filename,res,isLayered);
        int ticktime = std::stoi(res[1]); 
        int amount = 0;
        std::fstream filereader(filename);
        if(filereader.good()){
            std::string line;
            while(!filereader.eof()){
                getline(filereader, line);
                if(std::regex_search(line, res, element)) {
                    //std::cout << res[1] <<":" << res[2] << "\n";
                    data[(ticktime / 5) - 1][std::stoi(res[1])] = std::stoi(res[2]);
                    amount +=  1000 - std::stoi(res[2]);
                }

                
            }
        }
        std::cout << "ticktime "<< ticktime <<  "  lost : "  << amount << "\n"; 
        filereader.close();
    }

    public:
    TimeFrameLossTickTimeEPNRatio(){
        DIR *dir;
        
        struct dirent *ent = nullptr;
        if ((dir = opendir ("./")) != nullptr) {
             while ((ent = readdir (dir)) != nullptr) {
                 if(std::regex_match(ent->d_name, isLayered)){
                     loadFile(ent->d_name);
                    //printf ("%s\n", ent->d_name);
                 }
             }
        }
    }

};

void showTable(const TimeFrameLossTickTimeEPNRatio tf){
    std::cout << "EPNs\t\t|";
    for (int i = 0; i < CRASHED_EPNS; i++){
        std::cout << i << "   | ";
    }
    std::cout << "\n";
    for(int i = 0; i < TOTAL_TICKTIME / 5; i++) {
        std::cout << "ticktime\t| " << 5 + (i * 5) << " | ";
        for (int j = 0; j < CRASHED_EPNS; j++){
             std::cout << 1000 - tf.data[i][j] << " & ";
        }
       std::cout << "\n";
    }
}

TCanvas* LayeredView (){
    TimeFrameLossTickTimeEPNRatio ratio;
    showTable(ratio);
    TCanvas *c = new TCanvas("c","Graph2D example",0,0,600,400);
    Double_t x, y, z, P = 6.;
    Int_t np = 200;
    TGraph2D *dt = new TGraph2D();
    dt->SetTitle("Graph TF loss EPN/Ticktime ratio; ticktime; amount crashed epns; TF loss");

    Int_t index = 0;
    for(int x = 0; x < TOTAL_TICKTIME / 5; x++) {
        for (int y = 0; y < CRASHED_EPNS; y++){
            dt->SetPoint(index, 5 + x * 5,y + 1,(1000 - ratio.data[x][y]));
            index++;
        }
    }
      gStyle->SetPalette(1);
    dt->Draw("surf1");
 //dt->Draw("pcol");
    return c;
}