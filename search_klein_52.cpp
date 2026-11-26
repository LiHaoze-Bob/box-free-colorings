// Reproduce the 52-layer search using only the C++17 standard library.
// c++ -O3 -std=c++17 search_klein_52.cpp -o /tmp/search_klein_52
// /tmp/search_klein_52
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <vector>

namespace {
using Word = std::uint64_t;
using Grid = std::array<int, 7>;  // columns, with bit zero denoting the first row
constexpr int row[4][5] = {{0,1,2,3,4}, {1,0,2,3,4}, {0,1,3,2,4}, {1,0,3,2,4}};
constexpr int col[4][7] = {{0,1,2,3,4,5,6}, {1,0,3,2,5,4,6},
                           {2,3,0,1,4,5,6}, {3,2,1,0,5,4,6}};
constexpr int flip[4] = {0,1,1,0};

int rowpair[5][5], colpair[7][7], slot_orbit[420], width[420], orbit_count;
bool matching[420];
std::vector<int> balanced, common[32][32];
struct Orbit { int size; Word seed; };
std::map<std::vector<int>, Orbit> representatives;

int popcount(int x) {
    int count = 0;
    for (; x; x &= x-1) ++count;
    return count;
}

void setup() {
    int id = 0;
    for (int i = 0; i < 5; ++i) for (int j = i+1; j < 5; ++j)
        rowpair[i][j] = rowpair[j][i] = id++;
    id = 0;
    for (int i = 0; i < 7; ++i) for (int j = i+1; j < 7; ++j)
        colpair[i][j] = colpair[j][i] = id++;
    std::fill_n(slot_orbit, 420, -1);
    for (int c = 0; c < 7; ++c) for (int d = c+1; d < 7; ++d)
        for (int r = 0; r < 5; ++r) for (int s = r+1; s < 5; ++s)
            for (int a = 0; a < 2; ++a) {
                const int slot = 20*colpair[c][d] + 2*rowpair[r][s] + a;
                if (slot_orbit[slot] >= 0) continue;
                for (int g = 0; g < 4; ++g) {
                    const int image = 20*colpair[col[g][c]][col[g][d]]
                                    + 2*rowpair[row[g][r]][row[g][s]] + (a^flip[g]);
                    slot_orbit[image] = orbit_count;
                }
                matching[orbit_count] = (r==0 && s==1) || (r==2 && s==3);
                ++orbit_count;
            }
    for (int s : slot_orbit) ++width[s];
    for (int a = 0; a < 32; ++a) {
        if (popcount(a) == 2 || popcount(a) == 3) balanced.push_back(a);
        for (int b = 0; b < 32; ++b)
            for (int r = 0; r < 5; ++r) for (int s = r+1; s < 5; ++s)
                for (int color = 0; color < 2; ++color) {
                    int pair = (1 << r) | (1 << s);
                    int cells = color ? (a&b) : (~(a|b));
                    if ((cells & pair) == pair) common[a][b].push_back(2*rowpair[r][s]+color);
                }
    }
}

void consider(const Grid& grid, int size) {
    std::array<int,10> labels{};
    int n = 0;
    for (int i = 0; i < 7; ++i) for (int j = i+1; j < 7; ++j) {
        int base = 20*colpair[i][j];
        for (int pair : common[grid[i]][grid[j]]) labels[n++] = slot_orbit[base+pair];
    }
    std::sort(labels.begin(), labels.begin()+n);
    std::vector<int> support;
    for (int i = 0; i < n;) {
        const int s = labels[i];
        int j = i+1;
        while (j < n && labels[j] == s) ++j;
        if (size*(j-i) != width[s]) return;
        support.push_back(s);
        i=j;
    }
    Word seed = 0;
    for (int c = 0; c < 7; ++c) seed |= Word(grid[c]) << (5*c);
    representatives.emplace(support, Orbit{size,seed});
}

// Enumerate minimum layers by column multiset before assigning column positions.
void full_orbits(Grid& grid, int depth, int start, int rectangles) {
    if (depth == 7) {
        if (rectangles == 8) {
            Grid perm = grid;
            do { consider(perm, 4); } while (std::next_permutation(perm.begin(), perm.end()));
        }
        return;
    }
    for (int idx = start; idx < static_cast<int>(balanced.size()); ++idx) {
        const int value = balanced[idx];
        int count = rectangles;
        for (int j = 0; j < depth; ++j) count += static_cast<int>(common[value][grid[j]].size());
        if (count > 8) continue;
        grid[depth] = value;
        full_orbits(grid, depth+1, idx, count);
    }
}

// A short orbit is fixed by the color-preserving involution, the fourth group
// element. Choose one column in each of its column cycles, then fill its mate.
void short_orbits(Grid& grid, int depth) {
    constexpr int cycles[4][2] = {{0,3},{1,2},{4,5},{6,6}};
    if (depth < 4) {
        const int a = cycles[depth][0], b = cycles[depth][1];
        for (int value : balanced) {
            int mate = 0;
            for (int i = 0; i < 5; ++i) mate |= ((value>>i)&1) << row[3][i];
            if (a == b && value != mate) continue;
            grid[a] = value;
            grid[b] = mate;
            short_orbits(grid, depth+1);
        }
        return;
    }
    // Search the tight case in which all row-pair defects are concentrated on
    // the two disjoint row pairs moved by the color-reversing generators.
    for (int r = 0; r < 5; ++r) for (int s = r+1; s < 5; ++s) {
        int defect = 0;
        const int pair = (1<<r) | (1<<s);
        for (int color = 0; color < 2; ++color) {
            int k = 0;
            for (int v : grid) if (((color ? v : ~v) & pair) == pair) ++k;
            defect += (k-1)*(k-2)/2;
        }
        const bool matched = (r==0 && s==1) || (r==2 && s==3);
        if (defect > static_cast<int>(matched)) return;
    }
    // Balanced columns have 28 colored pair incidences, so R = 8 + total defect.
    consider(grid, 2);
}

struct Choice { std::vector<int> support; Orbit orbit; int excess; };
struct Node { int left, right, up, down, column, choice; };
std::vector<Choice> choices;
std::vector<Node> nodes;
std::vector<int> selected;
int degree[421];
long long calls;

void cover(int c) {
    nodes[nodes[c].left].right = nodes[c].right;
    nodes[nodes[c].right].left = nodes[c].left;
    for (int i=nodes[c].down; i!=c; i=nodes[i].down)
        for (int j=nodes[i].right; j!=i; j=nodes[j].right) {
            nodes[nodes[j].up].down = nodes[j].down;
            nodes[nodes[j].down].up = nodes[j].up;
            --degree[nodes[j].column];
        }
}
void uncover(int c) {
    for (int i=nodes[c].up; i!=c; i=nodes[i].up)
        for (int j=nodes[i].left; j!=i; j=nodes[j].left) {
            ++degree[nodes[j].column];
            nodes[nodes[j].up].down = j;
            nodes[nodes[j].down].up = j;
        }
    nodes[nodes[c].left].right = c;
    nodes[nodes[c].right].left = c;
}

bool solve(int allowance, int height) {
    ++calls;
    if (height == 52) return true;
    int c = nodes[0].right;
    if (!c) return false;
    for (int j = nodes[c].right; j; j = nodes[j].right)
        if (degree[j] < degree[c] || (degree[j] == degree[c] && width[j-1] > width[c-1])) c=j;
    if (!degree[c] && allowance < width[c-1]) return false;
    cover(c);
    for (int i=nodes[c].down; i!=c; i=nodes[i].down) {
        const int id = nodes[i].choice;
        if (choices[id].excess > allowance) continue;
        for (int j=nodes[i].right; j!=i; j=nodes[j].right) cover(nodes[j].column);
        selected.push_back(id);
        if (solve(allowance-choices[id].excess, height+choices[id].orbit.size)) return true;
        selected.pop_back();
        for (int j=nodes[i].left; j!=i; j=nodes[j].left) uncover(nodes[j].column);
    }
    if (matching[c-1] && width[c-1]==2 && allowance>=2 && solve(allowance-2,height)) return true;
    uncover(c);
    return false;
}

void build_matrix() {
    for (const auto& item : representatives) {
        const auto& support = item.first;
        const Orbit orbit = item.second;
        int excess = -8*orbit.size;
        for (int s : support) excess += width[s];
        choices.push_back({support,orbit,excess});
    }
    representatives.clear();
    // Fixed Park-Miller shuffle, independent of platform rand() implementations.
    std::uint64_t state = 11;
    for (int i=static_cast<int>(choices.size())-1; i>0; --i) {
        state = (16807*state) % 2147483647;
        std::swap(choices[i], choices[state%(i+1)]);
    }
    std::size_t node_count = orbit_count+1;
    for (const auto& choice : choices) node_count += choice.support.size();
    nodes.reserve(node_count);
    for (int i=0; i<=orbit_count; ++i) nodes.push_back({i-1,i+1,i,i,i,-1});
    nodes[0].left=orbit_count;
    nodes[orbit_count].right=0;
    for (int id=0; id<static_cast<int>(choices.size()); ++id) {
        int first=static_cast<int>(nodes.size());
        for (int label : choices[id].support) {
            int c=1+label, n=static_cast<int>(nodes.size());
            nodes.push_back({n-1,n+1,nodes[c].up,c,c,id});
            nodes[nodes[c].up].down=n;
            nodes[c].up=n;
            ++degree[c];
        }
        nodes[first].left=static_cast<int>(nodes.size())-1;
        nodes.back().right=first;
    }
}
}  // namespace

int main() {
    setup();
    Grid grid{};
    short_orbits(grid,0);
    std::cout << "Two-layer orbit supports: " << representatives.size() << '\n';
    full_orbits(grid,0,0,0);
    build_matrix();
    std::cout << "Total supports: " << choices.size() << ", slot orbits: " << orbit_count << '\n';
    if (!solve(4,0)) return 1;
    std::cout << "Found 52 layers after " << calls << " search nodes\n";
    for (int id : selected) {
        const Orbit orbit=choices[id].orbit;
        std::cout << orbit.size;
        for (int r=0; r<5; ++r) {
            std::cout << ' ';
            for (int c=0; c<7; ++c) std::cout << ((orbit.seed>>(5*c+r))&1);
        }
        std::cout << '\n';
    }
}
