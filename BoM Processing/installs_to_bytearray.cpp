#include <stdio.h>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <string.h>


struct PostcodeInstalls
{
  char postcode[4];
  int dwellings = 0;
  int installs = 0;
  float cap_tot = 0;
  float cap_under10 = 0;
  float cap_10_100 = 0;
  float cap_over100 = 0;
};


int to_int(std::string in)
{
  in.erase(0, 1);
  in.erase(in.length() - 1, 1);
  return atoi(in.c_str());
}


int to_float(std::string in)
{
  in.erase(0, 1);
  in.erase(in.length() - 1, 1);
  return atof(in.c_str());
}


extern "C" int main(int argc, char** argv)
{

  std::ifstream infile("postcodes_1618.csv");
  std::ofstream outfile("out.bin", std::ios::binary);
  int headings = 0;
  while (!infile.eof())
  {
    std::string line;
    std::getline(infile, line, '\r');

    std::istringstream ss1(line);

    if (headings == 0)
    {
      //while (ss1)
      for (int i = 0; i < 8; ++i)
      {
      	std::string head;
        std::getline(ss1, head, ',');
        headings++;
      }
      continue;
    }

    std::string tokens[14];
    for (int i = 0; i < headings; ++i)
    {
      std::getline(ss1, tokens[i], ',');
    }

    if (tokens[0].size() != 6) continue;

    PostcodeInstalls i;
    for (int j = 0; j < 4; ++j)
      i.postcode[j] = tokens[0].c_str()[j + 1];
    i.installs = to_int(tokens[1]);
    i.dwellings = to_int(tokens[2]);
    i.cap_tot = to_float(tokens[4]);
    i.cap_under10 = to_float(tokens[5]);
    i.cap_10_100 = to_float(tokens[6]);
    i.cap_over100 = to_float(tokens[7]);

    outfile.write(&i.postcode[0], 4*sizeof(char));
    outfile.write(reinterpret_cast<const char*>(&i.installs), sizeof(int));
    outfile.write(reinterpret_cast<const char*>(&i.dwellings), sizeof(int));
    outfile.write(reinterpret_cast<const char*>(&i.cap_tot), sizeof(float));
    outfile.write(reinterpret_cast<const char*>(&i.cap_under10), sizeof(float));
    outfile.write(reinterpret_cast<const char*>(&i.cap_10_100), sizeof(float));
    outfile.write(reinterpret_cast<const char*>(&i.cap_over100), sizeof(float));

  }
}