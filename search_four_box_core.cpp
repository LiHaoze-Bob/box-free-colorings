// Recover 42 layers using only the first eleven layers of the supplied file.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

using Layer = std::array<int, 7>;
using Mask = std::uint64_t;
struct Slot { int r, s, a, b, color; };
const std::array<int, 5> row_action{1, 0, 3, 4, 2};
const Layer col_action{3, 2, 5, 4, 1, 0, 6};

int edge(int a, int b, int n) {
    if (a > b) std::swap(a, b);
    return a * (2 * n - a - 1) / 2 + b - a - 1;
}

int index(Slot s) {
    return 20 * edge(s.a, s.b, 7) + 2 * edge(s.r, s.s, 5) + s.color;
}

std::vector<Slot> rectangles(const Layer &layer) {
    std::vector<Slot> result;
    for (int a = 0; a < 7; ++a) for (int b = a + 1; b < 7; ++b)
        for (int r = 0; r < 5; ++r) for (int s = r + 1; s < 5; ++s) {
            int mask = (1 << r) | (1 << s);
            for (int color : {0, 1}) {
                int bits = color * mask;
                if ((layer[a] & mask) == bits && (layer[b] & mask) == bits)
                    result.push_back({r, s, a, b, color});
            }
        }
    return result;
}

std::array<Mask, 420> remaining_orbits(std::istream &input, std::vector<Layer> &prefix) {
    std::array<int, 420> used{}, image{};
    for (int i = 1; i <= 11; ++i) {
        std::string header;
        int number;
        if (!(input >> header >> number) || header != "Layer" || number != i)
            throw std::runtime_error("Expected eleven numbered prefix layers");
        Layer layer{};
        for (int r = 0; r < 5; ++r) {
            std::string row;
            input >> row;
            if (row.size() != 7 || row.find_first_not_of("01") != std::string::npos)
                throw std::runtime_error("Invalid prefix row");
            for (int c = 0; c < 7; ++c) layer[c] |= (row[c] - '0') << r;
        }
        prefix.push_back(layer);
        for (Slot s : rectangles(layer)) ++used[index(s)];
    }
    for (int a = 0; a < 7; ++a) for (int b = a + 1; b < 7; ++b)
        for (int r = 0; r < 5; ++r) for (int s = r + 1; s < 5; ++s)
            for (int z : {0, 1})
                image[index({r,s,a,b,z})] = index({row_action[r], row_action[s],
                                                   col_action[a], col_action[b], z});
    int n = 0;
    std::array<Mask, 420> orbits{};
    for (int s = 0; s < 420; ++s) if (!used[s] && !orbits[s]) {
        if (n >= 56) throw std::runtime_error("Too many residual orbits");
        int t = s, size = 0;
        do {
            if (used[t]) throw std::runtime_error("Residual set is not invariant");
            orbits[t] = Mask(1) << n;
            t = image[t];
            ++size;
        } while (s != t);
        if (size != 6) throw std::runtime_error("Expected an orbit of size six");
        ++n;
    }
    if (n != 56) throw std::runtime_error("Expected 56 residual orbits");
    return orbits;
}

struct Candidate { Mask slots; Layer seed; };

std::vector<Candidate> candidates(const std::array<Mask, 420> &orbits) {
    const Layer types[] = {
        {3,3,12,21,22,25,26}, {3,5,9,14,18,20,25}, {3,5,9,14,18,21,28},
        {3,5,10,12,19,22,25}, {3,5,10,13,19,22,24}, {3,5,10,13,22,24,25}
    };
    std::unordered_map<Mask, Layer> catalog;
    for (const Layer &type : types) {
        auto slots = rectangles(type);
        std::array<int, 5> rows{0,1,2,3,4};
        do {
            for (int flip : {0, 1}) {
                Layer words{};
                for (int j = 0; j < 7; ++j) for (int i = 0; i < 5; ++i)
                    words[j] |= (((type[j] >> i) & 1) ^ flip) << rows[i];
                auto relabeled = slots;
                for (Slot &s : relabeled) {
                    s.r = rows[s.r];
                    s.s = rows[s.s];
                    s.color ^= flip;
                }
                Layer cols{0,1,2,3,4,5,6};
                do {
                    Mask occupied = 0;
                    for (Slot s : relabeled) {
                        s.a = cols[s.a];
                        s.b = cols[s.b];
                        Mask bit = orbits[index(s)];
                        if (!bit || (occupied & bit)) break;
                        occupied |= bit;
                    }
                    if (__builtin_popcountll(occupied) != 8 || catalog.count(occupied)) continue;
                    Layer seed{};
                    for (int j = 0; j < 7; ++j) seed[cols[j]] = words[j];
                    catalog.emplace(occupied, seed);
                } while (std::next_permutation(cols.begin(), cols.end()));
            }
        } while (std::next_permutation(rows.begin(), rows.end()));
    }
    std::vector<Candidate> result;
    for (auto item : catalog) result.push_back({item.first, item.second});
    std::sort(result.begin(), result.end(), [](auto a, auto b) { return a.slots < b.slots; });
    return result;
}

bool complete(Mask remaining, const std::vector<Candidate> &rows, std::vector<Layer> &solution) {
    if (!remaining) return true;
    std::array<int, 56> frequencies{};
    for (const auto &row : rows)
        for (Mask m = row.slots; m; m &= m - 1) ++frequencies[__builtin_ctzll(m)];
    int chosen = __builtin_ctzll(remaining);
    for (Mask m = remaining; m; m &= m - 1) {
        int k = __builtin_ctzll(m);
        if (frequencies[k] < frequencies[chosen]) chosen = k;
    }
    if (!frequencies[chosen]) return false;
    for (const auto &row : rows) if ((row.slots >> chosen) & 1) {
        std::vector<Candidate> compatible;
        for (const auto &other : rows)
            if (!(row.slots & other.slots)) compatible.push_back(other);
        solution.push_back(row.seed);
        if (complete(remaining ^ row.slots, compatible, solution)) return true;
        solution.pop_back();
    }
    return false;
}

// Keep two six-layer orbits in addition to the eleven-layer prefix.
// Count distinct partitions of the 40 residual slot orbits into five tiles.
void count_family(const std::array<Mask, 420>& orbits, const std::vector<Candidate>& rows) {
    const Layer locked_seeds[] = {{6,20,9,26,24,13,19}, {10,6,11,22,28,17,5}};
    Mask remaining = (Mask(1) << 56) - 1;
    for (const Layer& seed : locked_seeds) {
        Mask tile = 0;
        for (Slot slot : rectangles(seed)) tile |= orbits[index(slot)];
        if (__builtin_popcountll(tile) != 8 || (tile & remaining) != tile)
            throw std::runtime_error("Locked seed does not develop to a disjoint orbit");
        remaining ^= tile;
    }
    std::vector<Mask> tiles;
    std::array<unsigned, 56> frequencies{};
    for (const auto& row : rows) {
        if (row.slots & ~remaining) continue;
        tiles.push_back(row.slots);
        for (Mask m = row.slots; m; m &= m-1) ++frequencies[__builtin_ctzll(m)];
    }
    int pivot = __builtin_ctzll(remaining);
    for (Mask m = remaining; m; m &= m-1) {
        int j = __builtin_ctzll(m);
        if (frequencies[j] < frequencies[pivot]) pivot = j;
    }

    std::uint64_t total = 0;
    for (Mask first : tiles) {
        if (!(first & (Mask(1) << pivot))) continue;
        const Mask rest = remaining ^ first;
        std::vector<Mask> compatible;
        for (Mask tile : tiles) if (!(first & tile)) compatible.push_back(tile);
        std::unordered_map<Mask, unsigned> pairs;
        for (std::size_t i = 0; i < compatible.size(); ++i) {
            for (std::size_t j = 0; j < i; ++j) {
                Mask a = compatible[i], b = compatible[j];
                if (!(a & b)) ++pairs[a | b];
            }
        }
        std::uint64_t ordered_splits = 0;
        for (const auto& [part, ways] : pairs) {
            auto other = pairs.find(rest ^ part);
            if (other != pairs.end()) ordered_splits += std::uint64_t(ways) * other->second;
        }
        // Each four-tile partition has six choices of the first pair.
        if (ordered_splits % 6) throw std::runtime_error("Incomplete four-tile partition count");
        total += ordered_splits / 6;
    }
    std::cout << tiles.size() << " possible tiles on 40 residual orbits, "
              << total << " partitions into five tiles\n";
    if (tiles.size() != 9007 || total != 15907)
        throw std::runtime_error("Unexpected family count");
}

int main(int argc, char **argv) {
    std::ifstream input(argc > 1 ? argv[1] : "5x7x53_four_box_certificate.txt");
    std::vector<Layer> stack;
    auto orbits = remaining_orbits(input, stack);
    auto rows = candidates(orbits);
    if (argc > 2) {
        if (argc != 3 || std::string(argv[2]) != "--count-family")
            throw std::runtime_error("Usage: search_four_box_core [certificate [--count-family]]");
        count_family(orbits, rows);
        return 0;
    }
    std::vector<Layer> solution;
    if (!complete((Mask(1) << 56) - 1, rows, solution))
        throw std::runtime_error("Could not complete the given prefix");
    std::cout << rows.size() << " candidate supports, seven six-layer orbits\n";
    for (const auto &seed : solution) {
        for (int j = 0; j < 7; ++j) std::cout << (j ? " " : "") << seed[j];
        std::cout << '\n';
        Layer current = seed;
        for (int k = 0; k < 6; ++k) {
            stack.push_back(current);
            Layer next{};
            for (int j = 0; j < 7; ++j) for (int i = 0; i < 5; ++i)
                next[col_action[j]] |= ((current[j] >> i) & 1) << row_action[i];
            current = next;
        }
    }
    std::array<int, 420> counts{};
    for (const auto &layer : stack)
        for (Slot slot : rectangles(layer)) ++counts[index(slot)];
    if (stack.size() != 53 || std::count(counts.begin(), counts.end(), 1) != 416 ||
        std::count(counts.begin(), counts.end(), 2) != 4)
        throw std::runtime_error("Unexpected completed-stack multiplicities");
}
