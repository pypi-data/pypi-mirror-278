#include<iostream>
#include<fstream>
#include<vector>
#include<algorithm>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

using namespace std;
namespace py = pybind11;


vector<string> subset_gvcf(string filename, vector<int> positions){
    vector<string> header;
    vector<string> output;
    fstream fin(filename, fstream::in);
    if(!fin.good()){
        throw invalid_argument("Invalid gvcf path: " + filename);
    }
    char ch;
    string acc;
    size_t pos = 0;
    while (fin >> noskipws >> ch) {
        if(ch == '\n'){
            if(acc[0] == '#'){
                header.push_back(acc);
                acc = "";
                continue;
            }
            // Pull out the second column (which should be the position)
            string line = acc;
            pos = acc.find("\t");
            acc.erase(0, pos + 1);
            pos = acc.find("\t");
            string p = acc.substr(0, pos);
            int genome_pos = stoi(p);

            if(binary_search(positions.begin(), positions.end(), genome_pos)){
                output.push_back(line);
            }

            acc = "";
        }
        else{
            acc += ch;
        }
    }
    fin.close();
    header.insert( header.end(), output.begin(), output.end() );
    return header;

}

PYBIND11_MODULE(vcf_subset, m) {
    m.doc() =  R"pbdoc(
        Efficient VCF subsetting by genome position.
        Designed for subsetting a gVCF file, but should work for any VCF.
        -----------------------
           subset_gvcf
    )pbdoc";
    #ifdef VERSION_INFO
        m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
    #else
        m.attr("__version__") = "dev";
    #endif
    m.def("subset_vcf", &subset_gvcf, R"pbdoc(
        Subset a given VCF file to just the given positions (and the header).
        -----------------------

        Args:
            str filename: Path to the VCF file to subset. Must not be gzipped.
            list[int] positions: List of genome positions to keep
        
        Returns:
            list[str]: Lines of the VCF file that match the given positions (and the header)
        )pbdoc", py::arg("filename"), py::arg("positions"));
}