// Exhaust the 919-layer single-slot switch closure from the published 263-layer witness.
// Build: c++ -O3 -std=c++17 check_switched_pool.cpp -o /tmp/check_switched_pool
// Run: /tmp/check_switched_pool 5x7_multiplicity_certificates.txt
#include <algorithm>
#include <array>
#include <bitset>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

using Layer = std::array<unsigned, 7>;
using Slots = std::bitset<420>;
using Candidates = std::bitset<919>;

struct Entry {
    std::array<int, 8> slots;
    Slots mask;
};

Entry entry(const Layer& layer) {
    Entry out{};
    std::size_t count = 0;
    int pair = 0;
    for (int i = 0; i < 5; ++i) {
        for (int j = i + 1; j < 5; ++j, ++pair) {
            int edge = 0;
            unsigned rows = (1U << i) | (1U << j);
            for (int a = 0; a < 7; ++a) {
                for (int b = a + 1; b < 7; ++b, ++edge) {
                    unsigned x = layer[a] & rows, y = layer[b] & rows;
                    if (x == y && (x == 0 || x == rows)) {
                        int s = 21 * (2 * pair + (x == rows)) + edge;
                        out.slots.at(count++) = s;
                        out.mask.set(s);
                    }
                }
            }
        }
    }
    if (count != 8) throw std::runtime_error("expected a minimum layer");
    return out;
}

std::vector<Entry> read_pool(const char* filename) {
    const std::string digits = "0123456789abcdefghijklmnopqrstuv";
    std::ifstream f(filename);
    std::set<Layer> pool;
    int first, last;
    while (f >> first >> last) {
        for (int k = 0; k < last; ++k) {
            std::string word;
            f >> word;
            if (last != 263) continue;
            Layer layer;
            if (word.size() != 7) throw std::runtime_error("bad layer width");
            for (int j = 0; j < 7; ++j) {
                auto index = digits.find(word[j]);
                if (index == std::string::npos) throw std::runtime_error("bad layer word");
                layer[j] = static_cast<unsigned>(index);
            }
            pool.insert(layer);
        }
    }
    if (pool.size() != 263) throw std::runtime_error("expected 263 source layers");
    std::vector<Layer> queue(pool.begin(), pool.end());
    for (std::size_t k = 0; k < queue.size(); ++k) {
        auto layer = queue[k];
        const auto before = entry(layer).mask;
        for (int a = 0; a < 7; ++a) {
            for (int b = a + 1; b < 7; ++b) {
                std::swap(layer[a], layer[b]);
                if ((entry(layer).mask ^ before).count() <= 2 && pool.insert(layer).second)
                    queue.push_back(layer);
                std::swap(layer[a], layer[b]);
            }
        }
    }
    if (pool.size() != 919) throw std::runtime_error("expected a closure of size 919");
    std::vector<Entry> entries;
    for (const auto& layer : pool) entries.push_back(entry(layer));
    return entries;
}

class Search {
    const std::vector<Entry>& layers;
    std::array<Candidates, 420> incident{};
    std::array<Candidates, 20> by_label{};
    std::array<int, 20> target{};

    bool visit(int left, const Slots& covered, Candidates available,
               const std::array<int, 20>& need, unsigned doubled) const {
        if (left == 0) return covered.all();
        for (int p = 0; p < 20; ++p) {
            if (need[p] < 0 || need[p] > left) return false;
            if (need[p] == left) available &= by_label[p];
        }

        int pivot = -1;
        std::size_t best = layers.size() + 1;
        for (int s = 0; s < 420; ++s) {
            if (covered[s]) continue;
            auto count = (available & incident[s]).count();
            if (count == 0) return false;
            if (count < best) {
                best = count;
                pivot = s;
            }
        }
        if (pivot < 0) return false;
        const Candidates choices = available & incident[pivot];
        for (std::size_t i = 0; i < layers.size(); ++i) {
            if (!choices[i]) continue;
            const auto& layer = layers[i];
            auto next_available = available;
            auto next_need = need;
            unsigned next_doubled = doubled;
            for (int s : layer.slots) {
                int label = s / 21;
                --next_need[label];
                if (covered[s]) {
                    // This consumes the label's one permitted repeat. All its
                    // covered slots now forbid any further incidence.
                    next_doubled |= 1U << label;
                    for (int t = 21 * label; t < 21 * (label + 1); ++t)
                        if (covered[t]) next_available &= ~incident[t];
                }
                if (target[label] == 21 || (next_doubled & (1U << label)))
                    next_available &= ~incident[s];
            }
            if (visit(left - 1, covered | layer.mask, next_available, next_need, next_doubled))
                return true;
        }
        return false;
    }

public:
    explicit Search(const std::vector<Entry>& entries) : layers(entries) {
        for (std::size_t i = 0; i < layers.size(); ++i) {
            for (int s : layers[i].slots) {
                incident[s].set(i);
                by_label[s/21].set(i);
            }
        }
    }

    bool has_solution(unsigned high_rows) {
        int p = 0;
        for (int a = 0; a < 5; ++a) {
            for (int b = a + 1; b < 5; ++b, ++p) {
                bool x = high_rows & (1U << a), y = high_rows & (1U << b);
                target[2*p] = 21 + (!x && !y);
                target[2*p+1] = 21 + (x && y);
            }
        }
        Candidates all;
        all.set();
        return visit(53, Slots{}, all, target, 0);
    }
};

int main(int argc, char** argv) {
    auto layers = read_pool(argc > 1 ? argv[1] : "5x7_multiplicity_certificates.txt");
    Search search(layers);
    int excluded = 0;
    int from = argc > 2 ? std::stoi(argv[2]) : 0;
    int until = argc > 3 ? std::stoi(argv[3]) : 32;
    for (int high = from; high < until; ++high) {
        auto size = std::bitset<5>(high).count();
        if (size != 2 && size != 3) continue;
        if (search.has_solution(high)) {
            std::cerr << "A four-box stack exists for high-row mask " << high << '\n';
            return 1;
        }
        ++excluded;
        std::cout << "Excluded high-row mask " << high << std::endl;
    }
    std::cout << "Excluded a four-box substack for all " << excluded
              << " high-row sets in the 919-layer closure.\n";
}
