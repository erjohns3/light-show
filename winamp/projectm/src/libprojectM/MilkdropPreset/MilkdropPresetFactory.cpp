//
// C++ Implementation: MilkdropPresetFactory
//
// Description:
//
//
// Author: Carmelo Piccione <carmelo.piccione@gmail.com>, (C) 2008
//
// Copyright: See COPYING file that comes with this distribution
//
//
//
#include "MilkdropPresetFactory.hpp"

#include "MilkdropPreset.hpp"
#include "IdlePreset.hpp"

Preset*
MilkdropPresetFactory::LoadPresetFromFile(const std::string& filename)
{
    // std::cout << "MilkdropPresetFactory::LoadPresetFromFile " << filename << std::endl;

    std::string path;
    auto protocol = PresetFactory::Protocol(filename, path);
    if (protocol == "" || protocol == "file")
    {
        // std::cout << "MilkdropPresetFactory::LoadPresetFromFile  else if (protocol ==  || protocol == file)" << std::endl;
        // return std::make_unique<MilkdropPreset>(path);
        // create on heap
        auto preset = new MilkdropPreset(path);
        return preset;
    }
    else
    {
        // ToDO: Throw unsupported protocol exception instead to provide more information.
        return nullptr;
    }
}

std::unique_ptr<Preset> MilkdropPresetFactory::LoadPresetFromStream(std::istream& data)
{
    return std::make_unique<MilkdropPreset>(data);
}
