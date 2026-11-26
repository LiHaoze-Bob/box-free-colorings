// Exclude 24 complementary pairs and one pair with seven opposite rectangles.
// Build with a C++17 compiler. No input files or third-party libraries are needed.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <utility>
#include <vector>

using Layer = std::array<int, 7>;
using Slots = std::array<std::uint16_t, 8>;
using Edges = std::vector<std::array<int, 2>>;

Edges pairs(int n) {
    Edges result;
    for (int i = 0; i < n; ++i)
        for (int j = i + 1; j < n; ++j) result.push_back({i, j});
    return result;
}
const Edges rows = pairs(5), cols = pairs(7);
std::array<std::vector<int>, 32 * 32> agreements;

void require(bool condition, const char *reason) {
    if (!condition) throw std::runtime_error(reason);
}

void setup() {
    for (int x = 0; x < 32; ++x) for (int y = 0; y < 32; ++y)
        for (int p = 0; p < 10; ++p) for (int c = 0; c < 2; ++c) {
            int mask = (1 << rows[p][0]) | (1 << rows[p][1]);
            int desired = c ? mask : 0;
            if ((x & mask) == desired && (y & mask) == desired)
                agreements[32*x+y].push_back(2*p+c);
        }
}

std::set<Layer> minimum_multisets() {
    std::set<Layer> result;
    Layer words{};
    auto visit = [&](auto &self, int j, int start, int rectangles) -> void {
        if (j == 7) {
            if (rectangles == 8) result.insert(words);
            return;
        }
        for (int word = start; word < 32; ++word) {
            int ones = __builtin_popcount(static_cast<unsigned>(word));
            if (ones != 2 && ones != 3) continue;
            int total = rectangles;
            for (int i = 0; i < j; ++i) total += agreements[32*words[i]+word].size();
            if (total > 8) continue;
            words[j] = word;
            self(self, j+1, word, total);
        }
    };
    visit(visit, 0, 0, 0);
    return result;
}

std::set<Layer> representatives(std::set<Layer> remaining) {
    std::set<Layer> result;
    while (!remaining.empty()) {
        auto seed = *remaining.begin();
        result.insert(seed);
        std::array<int, 5> perm{0,1,2,3,4};
        do {
            for (int flip : {0,31}) {
                Layer image{};
                for (int j = 0; j < 7; ++j) {
                    image[j] = flip;
                    for (int i = 0; i < 5; ++i)
                        image[j] ^= ((seed[j] >> i) & 1) << perm[i];
                }
                std::sort(image.begin(), image.end());
                remaining.erase(image);
            }
        } while (std::next_permutation(perm.begin(), perm.end()));
    }
    return result;
}

Slots rectangles(const Layer &words) {
    Slots result{};
    int n = 0;
    for (int e = 0; e < 21; ++e)
        for (int label : agreements[32*words[cols[e][0]]+words[cols[e][1]]])
            result.at(n++) = 20*e + label;
    require(n == 8, "Unexpected rectangle count");
    return result;
}

struct Family {
    int high_rows = 0, blue_labels = 0;
    std::vector<Slots> layers;
    std::array<std::vector<std::uint16_t>, 420> containing;
};
std::vector<Family> families;
std::vector<int> first_layers;

void enumerate(const std::set<Layer> &multisets, const std::set<Layer> &seeds) {
    std::map<int,int> family_index;
    int total = 0;
    for (auto words : multisets) do {
        Slots slots = rectangles(words);
        int signature = 0;
        for (int s : slots) signature |= 1 << (s % 20);
        require(__builtin_popcount(static_cast<unsigned>(signature)) == 8,
                "A colored row pair occurs twice");
        auto inserted = family_index.emplace(signature, families.size());
        if (inserted.second) {
            Family family;
            for (int i = 0; i < 5; ++i) {
                int weight = 0;
                for (int w : words) weight += (w >> i) & 1;
                require(weight == 3 || weight == 4, "Unexpected row weight");
                if (weight == 4) family.high_rows |= 1 << i;
            }
            for (int p = 0; p < 10; ++p)
                if (signature & (1 << (2*p))) family.blue_labels |= 1 << p;
            families.push_back(std::move(family));
        }
        int group = inserted.first->second;
        auto &family = families[group];
        int index = family.layers.size();
        require(index < 65536, "Layer index overflows");
        if (seeds.count(words)) first_layers.push_back((group << 16) + index);
        for (int s : slots) family.containing[s].push_back(index);
        family.layers.push_back(slots);
        ++total;
    } while (std::next_permutation(words.begin(), words.end()));
    require(total == 4384800 && families.size() == 340 && first_layers.size() == 6,
            "Incomplete minimum-layer catalogue");
}

bool meets(int first, int second) {
    for (int i : cols[first]) for (int j : cols[second]) if (i == j) return true;
    return false;
}

// The signed row sums specify the two classes. The artificial 25-pair
// inventory supplies one additional constraint, the cut parity of its leave.
bool valid_rows(const Family &a, const Family &b, const Family &c,
                const std::set<int> &cuts) {
    int high = 0;
    for (int i = 0; i < 5; ++i) {
        int n = ((a.high_rows >> i) & 1) + ((b.high_rows >> i) & 1) + ((c.high_rows >> i) & 1);
        if (n != 1 && n != 2) return false;
        if (n == 2) high |= 1 << i;
    }
    int size = __builtin_popcount(static_cast<unsigned>(high));
    if (size != 2 && size != 3) return false;
    int h = a.blue_labels ^ b.blue_labels ^ c.blue_labels;
    for (int p = 0; p < 10; ++p)
        if (!(high & (1 << rows[p][0])) && !(high & (1 << rows[p][1]))) h ^= 1 << p;
    return cuts.count(h);
}

const Slots &lookup(int id) {return families[id >> 16].layers[id & 65535];}

int main() {
    setup();
    const auto multisets = minimum_multisets();
    require(multisets.size() == 900, "Unexpected minimum column multisets");
    enumerate(multisets, representatives(multisets));
    std::set<int> cuts;
    for (int mask = 0; mask < 32; ++mask) {
        int cut = 0;
        for (int p = 0; p < 10; ++p)
            cut |= (((mask >> rows[p][0]) ^ (mask >> rows[p][1])) & 1) << p;
        cuts.insert(cut);
    }
    int switches = 0;
    std::set<std::array<int,3>> six_tails, four_tails;
    for (int a : first_layers) {
        auto &x = lookup(a);
        std::array<bool,420> in_first{};
        for (int s : x) in_first[s] = true;
        for (int b_group = 0; b_group < static_cast<int>(families.size()); ++b_group) {
            const auto &family = families[b_group];
            std::vector<int> thirds;
            for (int g = 0; g < static_cast<int>(families.size()); ++g)
                if (valid_rows(families[a >> 16], family, families[g], cuts)) thirds.push_back(g);
            for (int j = 0; j < static_cast<int>(family.layers.size()); ++j) {
                const auto &y = family.layers[j];
                int same = 0, opposite = 0;
                for (int s : y) {same += in_first[s]; opposite += in_first[s ^ 1];}
                if (same == 7) {
                    int u = -1, v = -1;
                    for (int s : x) if (!std::binary_search(y.begin(), y.end(), s)) u = s;
                    for (int s : y) if (!in_first[s]) v = s;
                    require(u % 20 == v % 20 && meets(u/20, v/20), "Unexpected single-slot switch");
                    ++switches;
                }
                int b = (b_group << 16) + j;
                if (b == a || opposite < 3 || opposite > 7 || thirds.empty()) continue;
                std::array<int,210> difference{};
                for (int s : x) difference[s/2] += (s & 1) ? 1 : -1;
                for (int s : y) difference[s/2] += (s & 1) ? 1 : -1;
                std::vector<int> reverse;
                for (int q = 0; q < 210; ++q)
                    if (difference[q]) reverse.push_back(2*q + (difference[q] < 0));
                int required = 9 - opposite;
                for (int g : thirds) {
                    const auto &third = families[g];
                    std::vector<const std::vector<std::uint16_t> *> lists;
                    for (int s : reverse)
                        if (!third.containing[s].empty()) lists.push_back(&third.containing[s]);
                    if (static_cast<int>(lists.size()) < required) continue;
                    std::sort(lists.begin(), lists.end(), [](auto p, auto q){return p->size() < q->size();});
                    // A layer meeting at least 'required' lists meets one of
                    // the first n-required+1, since only required-1 remain.
                    lists.resize(lists.size()-required+1);
                    for (auto list : lists) for (int k : *list) {
                        int c = (g << 16) + k;
                        if (c == a || c == b) continue;
                        const auto &z = third.layers[k];
                        int hits = 0;
                        for (int s : z) hits += (s & 1) ? difference[s/2] < 0 : difference[s/2] > 0;
                        if (hits < required) continue;
                        auto final = difference;
                        for (int s : z) final[s/2] += (s & 1) ? 1 : -1;
                        int norm = 0;
                        for (int value : final) norm += std::abs(value);
                        std::array<int,3> triple{a,b,c};
                        std::sort(triple.begin(), triple.end());
                        if (norm == 4) four_tails.insert(triple);
                        if (norm != 6 || !six_tails.insert(triple).second) continue;
                        bool found = false;
                        for (int p = 0; p < 210; ++p) if (final[p] > 0)
                            for (int q = p % 10; q < 210; q += 10) if (final[q] < 0) {
                                require(!meets(p/10, q/10), "A signed defect admits an adjacent switch");
                                found = true;
                            }
                        require(found, "No signed defect pair");
                    }
                }
            }
        }
    }
    require(switches == 3 && four_tails.empty() && six_tails.size() == 64,
            "Unexpected normalized switch or triple counts");
    std::cout << switches << " normalized one-slot switches; all use adjacent column edges.\n"
              << four_tails.size() << " parity-compatible normalized triples of norm four; "
              << six_tails.size() << " of norm six.\n"
              << "Every opposite-sign defect pair on one row pair uses disjoint column edges.\n";
}
