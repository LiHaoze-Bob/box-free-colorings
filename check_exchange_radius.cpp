// Exhaustive +1 exchanges from a box-free 5-by-7 certificate.
// Compile: c++ -std=c++17 -O3 -march=native check_exchange_radius.cpp -o /tmp/check_exchange
// Run: /tmp/check_exchange CERTIFICATE RADIUS    (radius 0..6)
#include <algorithm>
#include <array>
#include <cstdint>
#include <deque>
#include <fstream>
#include <iostream>
#include <memory>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

using Word = std::uint64_t;
using Layer = std::array<int, 5>;
using Signature = std::array<Word, 7>;
constexpr int max_radius = 6;
constexpr int row_words = 128;
constexpr int slot_count = 420;

int popcount(Word v) { return __builtin_popcountll(v); }
int first_bit(Word v) { return __builtin_ctzll(v); }

struct Candidate {
    Signature slots;
    Layer rows;
    int next;
};

class Exchanges {
    const std::vector<Layer> base;
    const int radius;
    const int rectangle_limit;
    std::set<Layer> originals;
    Word rowslots[row_words][row_words]{};
    Word blockers[5][5][row_words][row_words]{};
    int choose[54][max_radius + 1]{};
    int offset[max_radius + 1]{};
    std::vector<int> head;
    std::deque<Candidate> catalog;
    std::array<long long, max_radius + 1> catalog_counts{}, deletion_counts{};
    Layer layer{};
    std::vector<int> options, selected, deleted;

    Signature signature(const Layer& rows) const {
        Signature bits{};
        int offset = 0;
        for (int i = 0; i < 5; ++i) {
            for (int j = i + 1; j < 5; ++j, offset += 42) {
                const Word mask = rowslots[rows[i]][rows[j]];
                bits[offset / 64] |= mask << (offset % 64);
                if (offset % 64 > 22) bits[offset / 64 + 1] |= mask >> (64 - offset % 64);
            }
        }
        return bits;
    }

    static bool disjoint(const Signature& a, const Signature& b) {
        for (int i = 0; i < 7; ++i) if (a[i] & b[i]) return false;
        return true;
    }

    void list_layers(int depth, Word blocked, int rectangles) {
        if (depth == 5) {
            if (originals.count(layer)) return;
            int size = 0, rank = 0;
            for (Word t = blocked; t; t &= t - 1) rank += choose[first_bit(t)][++size];
            int& first = head[offset[size] + rank];
            catalog.push_back({signature(layer), layer, first});
            first = static_cast<int>(catalog.size()) - 1;
            ++catalog_counts[size];
            return;
        }
        for (int row = 0; row < row_words; ++row) {
            Word next = blocked;
            for (int i = 0; i < depth; ++i) next |= blockers[i][depth][layer[i]][row];
            if (popcount(next) > radius) continue;
            int count = rectangles;
            for (int i = 0; i < depth; ++i) count += popcount(rowslots[layer[i]][row]);
            if (count > rectangle_limit) continue;
            layer[depth] = row;
            list_layers(depth + 1, next, count);
        }
    }

    bool pack(const std::vector<int>& pool, int need) {
        if (static_cast<int>(pool.size()) < need) return false;
        if (need == 1) {
            selected.push_back(pool.front());
            return true;
        }
        // Every layer needs at least eight distinct slots.
        Signature possible{};
        for (int id : pool) {
            for (int i = 0; i < 7; ++i) possible[i] |= catalog[id].slots[i];
        }
        int available = 0;
        for (Word w : possible) available += popcount(w);
        if (available < 8 * need) return false;
        for (std::size_t i = 0; i + need <= pool.size(); ++i) {
            std::vector<int> next;
            const auto& a = catalog[pool[i]].slots;
            for (std::size_t j = i + 1; j < pool.size(); ++j)
                if (disjoint(a, catalog[pool[j]].slots)) next.push_back(pool[j]);
            if (pack(next, need - 1)) {
                selected.push_back(pool[i]);
                return true;
            }
        }
        return false;
    }

    struct Subset { int size, rank; };
    using Subsets = std::array<Subset, 1 << max_radius>;

    bool visit(int start, const Subsets& subsets) {
        const int depth = static_cast<int>(deleted.size());
        ++deletion_counts[depth];
        if (pack(options, depth + 1)) return true;
        if (depth == radius) return false;
        for (int i = start; i < static_cast<int>(base.size()); ++i) {
            const auto previous_size = options.size();
            Subsets extended = subsets;
            for (int mask = 0; mask < (1 << depth); ++mask) {
                const int size = subsets[mask].size + 1;
                const int rank = subsets[mask].rank + choose[i][size];
                extended[mask + (1 << depth)] = {size, rank};
                int bucket = head[offset[size] + rank];
                for (int id = bucket; id >= 0; id = catalog[id].next) options.push_back(id);
            }
            deleted.push_back(i);
            if (visit(i + 1, extended)) return true;
            deleted.pop_back();
            options.resize(previous_size);
        }
        return false;
    }

public:
    Exchanges(const std::vector<Layer>& layers, int depth)
        : base(layers), radius(depth), rectangle_limit(slot_count - 8 * static_cast<int>(layers.size())),
          originals(layers.begin(), layers.end()) {
        const int n = static_cast<int>(base.size());
        if (n < 1 || n > 52 || radius < 0 || radius > max_radius)
            throw std::runtime_error("Expected 1..52 layers and a radius in 0..6");
        for (int i = 0; i <= n; ++i) {
            choose[i][0] = 1;
            for (int j = 1; j <= std::min(i, radius); ++j)
                choose[i][j] = choose[i - 1][j] + choose[i - 1][j - 1];
        }
        for (int j = 1; j <= radius; ++j) offset[j] = offset[j - 1] + choose[n][j - 1];
        head.assign(offset[radius] + choose[n][radius], -1);
        for (int a = 0; a < row_words; ++a) for (int b = 0; b < row_words; ++b) {
            int pos = 0;
            for (int c = 0; c < 7; ++c) for (int d = c + 1; d < 7; ++d, ++pos) {
                const int pair = (1 << c) | (1 << d);
                if (((a | b) & pair) == 0) rowslots[a][b] |= Word(1) << (2 * pos);
                if (((a & b) & pair) == pair) rowslots[a][b] |= Word(1) << (2 * pos + 1);
            }
        }
        Signature used{};
        for (int k = 0; k < n; ++k) {
            auto sig = signature(base[k]);
            if (!disjoint(used, sig)) throw std::runtime_error("Input contains a monochromatic box");
            for (int i = 0; i < 7; ++i) used[i] |= sig[i];
            for (int i = 0; i < 5; ++i) for (int j = i + 1; j < 5; ++j) {
                const Word old = rowslots[base[k][i]][base[k][j]];
                for (int a = 0; a < row_words; ++a) for (int b = 0; b < row_words; ++b)
                    if (old & rowslots[a][b]) blockers[i][j][a][b] |= Word(1) << k;
            }
        }
    }

    void run() {
        list_layers(0, 0, 0);
        for (int id = head[0]; id >= 0; id = catalog[id].next) options.push_back(id);
        if (visit(0, {})) {
            std::cout << "Delete original layers (one-based):";
            for (int k : deleted) std::cout << ' ' << k + 1;
            std::cout << "\nInsert these layers (five row integers each):\n";
            for (int id : selected) {
                for (int row : catalog[id].rows) std::cout << row << ' ';
                std::cout << '\n';
            }
            return;
        }
        std::cout << "deletions  non-original layers with exactly this many blockers  deletion sets\n";
        for (int k = 0; k <= radius; ++k)
            std::cout << k << ' ' << catalog_counts[k] << ' ' << deletion_counts[k] << '\n';
        std::cout << "No augmenting exchange through radius " << radius << '\n';
    }
};

int main(int argc, char** argv) {
    try {
        if (argc != 3) throw std::runtime_error("Usage: check_exchange CERTIFICATE RADIUS");
        std::ifstream input(argv[1]);
        if (!input) throw std::runtime_error("Cannot open certificate");
        std::vector<Layer> base;
        std::string line;
        while (std::getline(input, line)) {
            if (line.empty() || line[0] == '#') continue;
            if (line.rfind("Layer ", 0) != 0) throw std::runtime_error("Expected a layer header");
            Layer layer{};
            for (int& row : layer) {
                if (!std::getline(input, line) || line.size() != 7 ||
                    line.find_first_not_of("01") != std::string::npos)
                    throw std::runtime_error("Expected seven binary digits in every row");
                row = std::stoi(line, nullptr, 2);
            }
            base.push_back(layer);
        }
        // The row-pair blocker tables occupy several megabytes.
        auto search = std::make_unique<Exchanges>(base, std::stoi(argv[2]));
        search->run();
    } catch (const std::exception& e) {
        std::cerr << e.what() << '\n';
        return 1;
    }
}
