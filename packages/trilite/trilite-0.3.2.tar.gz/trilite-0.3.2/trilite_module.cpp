#include <bits/stdc++.h>

#ifndef TRILITE_GENERATOR_H
#define TRILITE_GENERATOR_H

#include <coroutine>
#include <iostream>
#include <optional>
#include <vector>

namespace TL {
// use Generator class from
// https://en.cppreference.com/w/cpp/coroutine/coroutine_handle while waiting
// for std::generator of c++23
template <std::movable T>
class Generator {
 public:
  struct promise_type {
    Generator<T> get_return_object() {
      return Generator{Handle::from_promise(*this)};
    }
    static std::suspend_always initial_suspend() noexcept { return {}; }
    static std::suspend_always final_suspend() noexcept { return {}; }
    std::suspend_always yield_value(T value) noexcept {
      current_value = std::move(value);
      return {};
    }
    // Disallow co_await in Generator coroutines.
    void await_transform() = delete;
    [[noreturn]]
    static void unhandled_exception() {
      throw;
    }

    std::optional<T> current_value;
  };

  using Handle = std::coroutine_handle<promise_type>;

  explicit Generator(const Handle coroutine) : m_coroutine{coroutine} {}

  Generator() = default;
  ~Generator() {
    if (m_coroutine) m_coroutine.destroy();
  }

  Generator(const Generator&) = delete;
  Generator& operator=(const Generator&) = delete;

  Generator(Generator&& other) noexcept : m_coroutine{other.m_coroutine} {
    other.m_coroutine = {};
  }
  Generator& operator=(Generator&& other) noexcept {
    if (this != &other) {
      if (m_coroutine) m_coroutine.destroy();
      m_coroutine = other.m_coroutine;
      other.m_coroutine = {};
    }
    return *this;
  }

  // Range-based for loop support.
  class Iter {
   public:
    void operator++() { m_coroutine.resume(); }
    const T& operator*() const { return *m_coroutine.promise().current_value; }
    bool operator==(std::default_sentinel_t) const {
      return !m_coroutine || m_coroutine.done();
    }

    explicit Iter(const Handle coroutine) : m_coroutine{coroutine} {}

   private:
    Handle m_coroutine;
  };

  Iter begin() {
    if (m_coroutine) m_coroutine.resume();
    return Iter{m_coroutine};
  }

  std::default_sentinel_t end() { return {}; }

 private:
  Handle m_coroutine;
};

/*template <std::movable T>
std::vector<T> ToVector(Generator<T> generator) {
  std::vector<T> out_vector;
  for (T t : generator) {
    out_vector.push_back(t);
  }
  return out_vector;
}
template <std::movable T>
std::vector<T> ToVector(Generator<T> generator) {
  std::vector<T> out_vector;
  for (T t : generator) {
    out_vector.push_back(t);
  }
  return out_vector;
}*/
template <std::movable T>
std::vector<T> ToVector(auto view) {
  std::vector<T> out_vector;
  for (T t : view) {
    out_vector.push_back(t);
  }
  return out_vector;
}
}  // namespace TL
#endif  // TRILITE_GENERATOR_H// MIT License
//
// Copyright (c) 2024 TriLite https://github.com/MeshLite/TriLite
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

#ifndef TRILITE_TRIMESH_HPP
#define TRILITE_TRIMESH_HPP

#include <Eigen/Eigen>
#include <memory>
#include <queue>
#include <ranges>
#include <unordered_set>

namespace TL {

enum MeshComponent { kHalfedge, kVertex, kFace };
using Index = unsigned int;
using H = Index;
using V = Index;
using F = Index;
constexpr Index kInvalidId = std::numeric_limits<Index>::max();
using Eigen::Vector3d;
/**
 * @class Trimesh
 * @brief Represents a triangle mesh using a half-edge data structure.
 */
class Trimesh {
 public:
  /**
   * @brief Constructs an empty Trimesh.
   */
  Trimesh();

  /**
   * @brief Constructs a Trimesh from a vector of vertices and their positions.
   * @param tri_points Vector of vertices and positions defining the triangle
   * mesh.
   */
  Trimesh(const std::vector<std::variant<V, Vector3d>>& tri_points);

  /**
   * @brief Copy constructor for Trimesh.
   * @param other The Trimesh object to copy.
   */
  Trimesh(const Trimesh& other);

  /**
   * @brief Assignment operator for Trimesh.
   * @param other The Trimesh object to assign.
   * @return A reference to the assigned Trimesh object.
   */
  Trimesh& operator=(const Trimesh& other);

  /**
   * @brief Returns the number of halfedges in the mesh.
   * @return The number of halfedges.
   */
  H NumHalfedges() const;

  /**
   * @brief Returns the number of vertices in the mesh.
   * @return The number of vertices.
   */
  V NumVertices() const;

  /**
   * @brief Returns the number of faces in the mesh.
   * @return The number of faces.
   */
  F NumFaces() const;

  /**
   * @brief Returns a view of the halfedges in the mesh.
   * @return A range of halfedge indices.
   */
  std::ranges::iota_view<H, H> Halfedges() const;

  /**
   * @brief Returns a view of the vertices in the mesh.
   * @return A range of vertex indices.
   */
  std::ranges::iota_view<V, V> Vertices() const;

  /**
   * @brief Returns a view of the faces in the mesh.
   * @return A range of face indices.
   */
  std::ranges::iota_view<F, F> Faces() const;

  /**
   * @brief Returns a view of the vertex positions.
   * @return A reference view of the vertex positions.
   */
  std::ranges::ref_view<std::vector<Vector3d>> Positions();

  /**
   * @brief Returns a constant view of the vertex positions.
   * @return A constant reference view of the vertex positions.
   */
  std::ranges::ref_view<const std::vector<Vector3d>> Positions() const;

  /**
   * @brief Returns the next halfedge in the face.
   * @param h The current halfedge.
   * @return The next halfedge in the face.
   */
  H HNext(H h) const;

  /**
   * @brief Returns the previous halfedge in the face.
   * @param h The current halfedge.
   * @return The previous halfedge in the face.
   */
  H HPrev(H h) const;

  /**
   * @brief Returns the starting vertex of the halfedge.
   * @param h The halfedge index.
   * @return The starting vertex index.
   */
  V HStart(H h) const;

  /**
   * @brief Returns the ending vertex of the halfedge.
   * @param h The halfedge index.
   * @return The ending vertex index.
   */
  V HEnd(H h) const;

  /**
   * @brief Returns the face associated with the halfedge.
   * @param h The halfedge index.
   * @return The face index.
   */
  F HFace(H h) const;

  /**
   * @brief Returns the opposite halfedge of the given halfedge.
   * @param h The halfedge index.
   * @return The opposite halfedge index or kInvalidId if it does not exist.
   */
  H HOpposite(H h) const;

  /**
   * @brief Returns the next halfedge around the starting vertex.
   * @param h The current halfedge.
   * @return The next halfedge around the starting vertex.
   */
  H HNextAroundStart(H h) const;

  /**
   * @brief Returns the previous halfedge around the starting vertex.
   * @param h The current halfedge.
   * @return The previous halfedge around the starting vertex.
   */
  H HPrevAroundStart(H h) const;

  /**
   * @brief Returns the next halfedge around the ending vertex.
   * @param h The current halfedge.
   * @return The next halfedge around the ending vertex.
   */
  H HNextAroundEnd(H h) const;

  /**
   * @brief Returns the previous halfedge around the ending vertex.
   * @param h The current halfedge.
   * @return The previous halfedge around the ending vertex.
   */
  H HPrevAroundEnd(H h) const;

  /**
   * @brief Returns the geometric vector of the halfedge.
   * @param h The halfedge index.
   * @return The geometric vector.
   */
  inline Vector3d HGeometry(H h) const;

  /**
   * @brief Computes the centroid (mean) position of a specific halfedge.
   * @param h The halfedge index for which to compute the centroid.
   * @return A Vector3d representing the centroid of the specified halfedge.
   */
  inline Vector3d HCentroid(H h) const;

  /**
   * @brief Returns a generator for the halfedges connected around the starting
   * vertex.
   * @param st_h The starting halfedge.
   * @return A generator for the connected halfedges.
   */
  Generator<H> HConnectionsAroundStart(H st_h) const;

  /**
   * @brief Returns a generator for the halfedges around a hole.
   * @param st_h The starting halfedge of the hole.
   * @return A generator for the halfedges around the hole.
   */
  Generator<H> HHalfedgesAroundHole(H st_h) const;

  /**
   * @brief Returns the length of the halfedge.
   * @param h The halfedge index.
   * @return The length of the halfedge.
   */
  double HLength(H h) const;

  /**
   * @brief Returns the starting halfedge of the vertex.
   * @param v The vertex index.
   * @return The starting halfedge index.
   */
  H VStarting(V v) const;

  /**
   * @brief Returns the ending halfedge of the vertex.
   * @param v The vertex index.
   * @return The ending halfedge index.
   */
  H VEnding(V v) const;

  /**
   * @brief Returns a generator for the starting halfedges of the vertex.
   * @param v The vertex index.
   * @return A generator for the starting halfedges.
   */
  Generator<H> VStartings(V v) const;

  /**
   * @brief Returns a generator for the ending halfedges of the vertex.
   * @param v The vertex index.
   * @return A generator for the ending halfedges.
   */
  Generator<H> VEndings(V v) const;

  /**
   * @brief Returns a view of the faces connected to the vertex.
   * @param v The vertex index.
   * @return A view of the face indices.
   */
  Generator<F> VFaces(V v) const;

  /**
   * @brief Returns the position of the vertex.
   * @param v The vertex index.
   * @return The position of the vertex.
   */
  Vector3d& VPosition(V v);

  /**
   * @brief Returns the constant position of the vertex.
   * @param v The vertex index.
   * @return The constant position of the vertex.
   */
  const Vector3d& VPosition(V v) const;

  /**
   * @brief Returns the normal vector of the vertex.
   * @param v The vertex index.
   * @return The normal vector.
   */
  Vector3d VNormal(V v) const;

  /**
   * @brief Returns the valence (degree) of the vertex.
   * @param v The vertex index.
   * @return The valence of the vertex.
   */
  size_t VValence(V v) const;

  /**
   * @brief Checks if the vertex is manifold.
   * @param v The vertex index.
   * @return True if the vertex is manifold, false otherwise.
   */
  bool VIsManifold(V v) const;

  /**
   * @brief Returns the halfedge associated with the face.
   * @param f The face index.
   * @return The halfedge index.
   */
  H FHalfedge(F f) const;

  /**
   * @brief Returns a view of the halfedges of the face.
   * @param f The face index.
   * @return A range of halfedge indices.
   */
  std::ranges::iota_view<H, H> FHalfedges(F f) const;

  /**
   * @brief Returns a generator for neighboring faces of a given face.
   * @param f The face index for which to find neighboring faces.
   * @return Generator<F> A generator for the indices of neighboring faces.
   */
  Generator<F> FNeighbors(F f) const;

  /**
   * @brief Returns a view of the vertices of the face.
   * @param f The face index.
   * @return A view of the vertex indices.
   */
  auto FVertices(F f) const;

  /**
   * @brief Returns a view of the vertex positions of the face.
   * @param f The face index.
   * @return A view of the vertex positions.
   */
  auto FPositions(F f) const;

  /**
   * @brief Returns the normal vector of the face.
   * @param f The face index.
   * @return The normal vector.
   */
  Vector3d FNormal(F f) const;

  /**
   * @brief Returns the area of the face.
   * @param f The face index.
   * @return The area of the face.
   */
  double FArea(F f) const;

  /**
   * @brief Computes the axis-aligned bounding box (AABB) of a specific face.
   * @param f The face index for which to compute the bounding box.
   * @return A pair of Vector3d, where the first element is the minimum corner
   * of the bounding box and the second element is the maximum corner of the
   * bounding box.
   */
  inline std::pair<Vector3d, Vector3d> FBoundingBox(F f) const;

  /**
   * @brief Computes the centroid (mean) of a specific face.
   * @param f The face index for which to compute the centroid.
   * @return A Vector3d representing the centroid of the specified face.
   */
  inline Vector3d FCentroid(F f) const;

  /**
   * @brief Returns a generator for the halfedges forming an edge.
   * @param h The halfedge index.
   * @return A generator for the halfedges forming the edge.
   */
  Generator<H> EdgeHalfedges(H h) const;

  /**
   * @brief Returns a view of the faces connected by an edge.
   * @param h The halfedge index.
   * @return A view of the face indices.
   */
  Generator<F> EdgeFaces(H h) const;

  /**
   * @brief Checks if the edge is manifold.
   * @param h The halfedge index.
   * @return True if the edge is manifold, false otherwise.
   */
  bool EdgeIsManifold(H h) const;

  /**
   * @brief Returns a view of the boundary halfedges.
   * @return A view of the boundary halfedge indices.
   */
  auto BoundaryHalfedges() const;

  /**
   * @brief Computes the axis-aligned bounding box (AABB) of the entire mesh.
   * @return A pair of Vector3d, where the first element is the minimum corner
   * of the bounding box and the second element is the maximum corner of the
   * bounding box.
   * @throws std::runtime_error if the mesh has no vertices.
   */
  std::pair<Vector3d, Vector3d> BoundingBox() const;

  /**
   * @brief Computes the centroid (mean) of all vertices in the mesh.
   * @return A Vector3d representing the centroid of all vertices in the mesh.
   * @throws std::runtime_error if the mesh has no vertices.
   */
  Vector3d Centroid() const;

  /**
   * @brief Adds a face to the mesh.
   * @param triangle Array of three vertices or positions defining the triangle.
   * @return The face index.
   */
  F AddFace(const std::array<std::variant<V, Vector3d>, 3>& triangle);

  /**
   * @brief Removes a face from the mesh.
   * @param f The face index.
   * @return A vector of vertices removed along with the face.
   */
  std::vector<V> RemoveFace(F f);

  /**
   * @brief Removes multiple face indices from the mesh.
   * @param f_set A vector of face indices to remove (duplicates are ignored).
   * @return A vector of vertices indices removed along with the faces in the
   * order of deletion (vertex indices must be updated accordingly on the fly).
   */
  std::vector<V> RemoveFaces(std::vector<F> f_set);

  /**
   * @brief Collapses an edge and merges its vertices.
   * @param h The halfedge index.
   * @return A pair of vectors containing the removed faces and vertices.
   */
  std::pair<std::vector<F>, std::vector<V>> CollapseEdge(H h);

  /**
   * @brief Splits an edge and the incident faces.
   * @param h The halfedge index.
   */
  void SplitEdge(H h);

  /**
   * @brief Flips an edge shared by two adjacent triangles.
   * @param h The halfedge index representing the edge to flip.
   */
  void FlipHalfedgeWithOpposite(H h);

  /**
   * @brief Disconnects a face from the mesh, converting it to a boundary
   * face.
   * @param f The face index.
   */
  void DisconnectFace(F f);

  /**
   * @brief Disconnects faces until all edges are manifold.
   */
  void DisconnectFacesUntilManifoldEdges();

  /**
   * @brief Disconnects faces until all vertices are manifold.
   */
  void DisconnectFacesUntilManifoldVertices();

  /**
   * @brief Disconnects faces until both edges and vertices are manifold.
   */
  void DisconnectFacesUntilManifold();

  /**
   * @brief Creates an attribute for a specified mesh component.
   * @tparam C The mesh component (halfedge, vertex, or face).
   * @tparam T The attribute type.
   * @param key The key identifying the attribute.
   * @return A reference view of the created attribute.
   * @throws std::invalid_argument if the attribute already exists.
   */
  template <MeshComponent C, typename T>
  std::ranges::ref_view<std::vector<T>> CreateAttribute(const std::string& key);

  /**
   * @brief Retrieves an attribute for a specified mesh component.
   * @tparam C The mesh component (halfedge, vertex, or face).
   * @tparam T The attribute type.
   * @param key The key identifying the attribute.
   * @return A reference view of the attribute.
   * @throws std::invalid_argument if the attribute does not exist or type does
   * not match.
   */
  template <MeshComponent C, typename T>
  std::ranges::ref_view<std::vector<T>> GetAttribute(const std::string& key);

  /**
   * @brief Erases an attribute for a specified mesh component.
   * @tparam C The mesh component (halfedge, vertex, or face).
   * @param key The key identifying the attribute.
   * @throws std::invalid_argument if the attribute does not exist.
   */
  template <MeshComponent C>
  void EraseAttribute(const std::string& key);

 private:
  class BaseContainerWrapper {
   public:
    virtual ~BaseContainerWrapper() = default;
    virtual std::unique_ptr<BaseContainerWrapper> clone() const = 0;
    virtual void ReplaceErase(int i) = 0;
    virtual void IncrementSize() = 0;
  };
  template <typename Container>
  class ContainerWrapper : public BaseContainerWrapper {
   public:
    Container container_;
    explicit ContainerWrapper(const Container& container)
        : container_(container) {}
    std::unique_ptr<BaseContainerWrapper> clone() const override {
      return std::make_unique<ContainerWrapper<Container>>(*this);
    }
    void ReplaceErase(int i) override {
      container_[i] = std::move(container_.back());
      container_.pop_back();
    }
    void IncrementSize() override { container_.emplace_back(); }
  };
  std::vector<V> hStart_;
  std::vector<H> hCoStart_;
  std::vector<H> vStart_;
  std::vector<Vector3d> position_;
  std::array<std::map<std::string, std::unique_ptr<BaseContainerWrapper>>, 3>
      attributes_;
};

Trimesh::Trimesh() {}
Trimesh::Trimesh(const std::vector<std::variant<V, Vector3d>>& tri_points)
    : Trimesh() {
  for (V v = 0; v < (V)tri_points.size(); v += 3) {
    AddFace({tri_points[v], tri_points[v + 1], tri_points[v + 2]});
  }
}
Trimesh::Trimesh(const Trimesh& other)
    : hStart_(other.hStart_),
      hCoStart_(other.hCoStart_),
      vStart_(other.vStart_),
      position_(other.position_) {
  for (int i = 0; i < 3; ++i) {
    for (const auto& [key, wrapper] : other.attributes_[i]) {
      attributes_[i][key] = wrapper->clone();
    }
  }
}
Trimesh& Trimesh::operator=(const Trimesh& other) {
  if (this != &other) {
    hStart_ = other.hStart_;
    hCoStart_ = other.hCoStart_;
    vStart_ = other.vStart_;
    position_ = other.position_;
    for (auto& attr_map : attributes_) {
      attr_map.clear();
    }
    for (int i = 0; i < 3; ++i) {
      for (const auto& [key, wrapper] : other.attributes_[i]) {
        attributes_[i][key] = wrapper->clone();
      }
    }
  }
  return *this;
}
inline H Trimesh::NumHalfedges() const { return hStart_.size(); }
inline V Trimesh::NumVertices() const { return position_.size(); }
inline F Trimesh::NumFaces() const { return NumHalfedges() / 3; }
inline std::ranges::iota_view<H, H> Trimesh::Halfedges() const {
  return std::views::iota(H{0}, H{NumHalfedges()});
}
inline std::ranges::iota_view<V, V> Trimesh::Vertices() const {
  return std::views::iota(V{0}, V{NumVertices()});
}
inline std::ranges::iota_view<F, F> Trimesh::Faces() const {
  return std::views::iota(F{0}, F{NumFaces()});
}
inline std::ranges::ref_view<std::vector<Vector3d>> Trimesh::Positions() {
  return std::views::all(position_);
}
inline std::ranges::ref_view<std::vector<Vector3d> const> Trimesh::Positions()
    const {
  return std::views::all(position_);
}
inline H Trimesh::HNext(H h) const {
  assert(h < NumHalfedges());
  return h - h % 3 + (h + 1) % 3;
}
inline H Trimesh::HPrev(H h) const {
  assert(h < NumHalfedges());
  return h - h % 3 + (h + 2) % 3;
}
inline V Trimesh::HStart(H h) const { return hStart_.at(h); }
inline V Trimesh::HEnd(H h) const { return HStart(HNext(h)); }
inline F Trimesh::HFace(H h) const {
  assert(h < NumHalfedges());
  return h / 3;
}
H Trimesh::HOpposite(H h) const {
  for (H nh : VStartings(HStart(HNext(h)))) {
    if (HEnd(nh) == HStart(h) && HStart(nh) == HEnd(h)) {
      return nh;
    }
  }
  return kInvalidId;
}
inline H Trimesh::HNextAroundStart(H h) const { return HOpposite(HPrev(h)); }
inline H Trimesh::HPrevAroundStart(H h) const {
  return HOpposite(h) == kInvalidId ? kInvalidId : HNext(HOpposite(h));
}
inline H Trimesh::HNextAroundEnd(H h) const {
  return HOpposite(h) == kInvalidId ? kInvalidId : HPrev(HOpposite(h));
}
inline H Trimesh::HPrevAroundEnd(H h) const { return HOpposite(HNext(h)); }
inline Vector3d Trimesh::HGeometry(H h) const {
  return VPosition(HEnd(h)) - VPosition(HStart(h));
}
inline Vector3d Trimesh::HCentroid(H h) const {
  return (VPosition(HEnd(h)) + VPosition(HStart(h))) / 2.0;
}
Generator<H> Trimesh::HConnectionsAroundStart(H st_h) const {
  H h = st_h;
  while (HOpposite(h) != kInvalidId) {
    assert(EdgeIsManifold(h));
    h = HPrevAroundStart(h);
    if (h == st_h) {
      break;
    }
  }
  st_h = h;
  do {
    assert(EdgeIsManifold(h));
    co_yield h;
    h = HNextAroundStart(h);
  } while (h != st_h && h != kInvalidId);
}
Generator<H> Trimesh::HHalfedgesAroundHole(H st_h) const {
  assert(HOpposite(st_h) == kInvalidId);
  H h = st_h;
  do {
    co_yield h;
    h = HNext(h);
    while (HOpposite(h) != kInvalidId) {
      assert(EdgeIsManifold(h));
      h = HPrevAroundStart(h);
    }
  } while (h != st_h);
}
inline double Trimesh::HLength(H h) const { return HGeometry(h).norm(); }
inline H Trimesh::VStarting(V v) const { return vStart_.at(v); }
inline H Trimesh::VEnding(V v) const { return HPrev(VStarting(v)); }
Generator<H> Trimesh::VStartings(V v) const {
  for (H h = VStarting(v); h != kInvalidId; h = hCoStart_[h]) {
    co_yield h;
  }
}
Generator<H> Trimesh::VEndings(V v) const {
  for (H h : VStartings(v)) {
    co_yield HPrev(h);
  }
}
Generator<F> Trimesh::VFaces(TL::V v) const {
  for (H h : VStartings(v)) {
    co_yield HFace(h);
  }
}
inline Vector3d& Trimesh::VPosition(V v) { return position_.at(v); }
inline const Vector3d& Trimesh::VPosition(V v) const { return position_.at(v); }
Vector3d Trimesh::VNormal(V v) const {
  Vector3d normal{Vector3d::Zero()};
  for (F f : VFaces(v)) {
    normal += FNormal(f);
  }
  return normal.normalized();
}
size_t Trimesh::VValence(V v) const {
  size_t ans = 0;
  for ([[maybe_unused]] H h : VStartings(v)) ans++;
  return ans;
}
bool Trimesh::VIsManifold(V v) const {
  int ct1 = 0;
  for ([[maybe_unused]] H h : HConnectionsAroundStart(VStarting(v))) {
    ++ct1;
  }
  int ct2 = 0;
  for ([[maybe_unused]] H h : VStartings(v)) {
    ++ct2;
  }
  return ct1 == ct2;
}
inline H Trimesh::FHalfedge(F f) const {
  assert(f < NumFaces());
  return 3 * f;
}
inline std::ranges::iota_view<H, H> Trimesh::FHalfedges(F f) const {
  return std::views::iota(FHalfedge(f), H{3 * f + 3});
}
Generator<F> Trimesh::FNeighbors(F f) const {
  for (H h : FHalfedges(f)) {
    H opp = HOpposite(h);
    if (opp != kInvalidId) {
      co_yield HFace(opp);
    }
  }
}
inline auto Trimesh::FVertices(F f) const {
  return std::views::transform(FHalfedges(f),
                               [this](H h) { return HStart(h); });
}
inline auto Trimesh::FPositions(F f) const {
  return std::views::transform(FVertices(f),
                               [this](V v) { return VPosition(v); });
}
inline Vector3d Trimesh::FNormal(F f) const {
  return HGeometry(3 * f).cross(-HGeometry(3 * f + 2)).normalized();
}
inline double Trimesh::FArea(F f) const {
  return 0.5 * HGeometry(3 * f).cross(HGeometry(3 * f + 2)).norm();
}
inline std::pair<Vector3d, Vector3d> Trimesh::FBoundingBox(F f) const {
  return {VPosition(HStart(3 * f))
              .cwiseMin(VPosition(HStart(3 * f + 1)))
              .cwiseMin(VPosition(HStart(3 * f + 2))),
          VPosition(HStart(3 * f))
              .cwiseMax(VPosition(HStart(3 * f + 1)))
              .cwiseMax(VPosition(HStart(3 * f + 2)))};
}
inline Vector3d Trimesh::FCentroid(F f) const {
  return (VPosition(HStart(3 * f)) + VPosition(HStart(3 * f + 1)) +
          VPosition(HStart(3 * f + 2))) /
         3.0;
}
Generator<H> Trimesh::EdgeHalfedges(H h) const {
  for (H he : VStartings(HStart(h))) {
    if (HEnd(he) == HEnd(h)) {
      co_yield (he);
    }
  }
  for (H he : VStartings(HEnd(h))) {
    if (HEnd(he) == HStart(h)) {
      co_yield (he);
    }
  }
}
Generator<F> Trimesh::EdgeFaces(H h) const {
  for (H h : EdgeHalfedges(h)) {
    co_yield HFace(h);
  }
}
bool Trimesh::EdgeIsManifold(H h) const {
  for (H g : EdgeHalfedges(h)) {
    if (g != h && g != HOpposite(h)) {
      return false;
    }
  }
  return true;
}
inline auto Trimesh::BoundaryHalfedges() const {
  return std::views::filter(Halfedges(),
                            [this](H h) { return HOpposite(h) == kInvalidId; });
}
std::pair<Vector3d, Vector3d> Trimesh::BoundingBox() const {
  if (position_.empty()) {
    throw std::runtime_error("Mesh has no vertices.");
  }
  Vector3d min = position_.front();
  Vector3d max = min;
  for (const auto& pos : position_) {
    min = min.cwiseMin(pos);
    max = max.cwiseMax(pos);
  }
  return {min, max};
}
Vector3d Trimesh::Centroid() const {
  if (position_.empty()) {
    throw std::runtime_error("Mesh has no vertices.");
  }
  Vector3d centroid = Vector3d::Zero();
  for (const auto& pos : position_) {
    centroid += pos;
  }
  centroid /= static_cast<double>(position_.size());
  return centroid;
}
F Trimesh::AddFace(const std::array<std::variant<V, Vector3d>, 3>& triangle) {
  for (int i = 0; i < 3; i++) {
    if (std::holds_alternative<V>(triangle[i])) {
      for (int j = 0; j < i; j++) {
        if (triangle[i] == triangle[j]) {
          throw std::invalid_argument(
              "AddFace called with a degenerated triangle parameter");
        }
      }
    }
  }
  for (const auto& [key, f_attr] : attributes_[kFace]) {
    f_attr->IncrementSize();
  }
  H h_offset = hStart_.size();
  for (const auto& elem : triangle) {
    H h = hStart_.size();
    V v = position_.size();
    if (std::holds_alternative<V>(elem)) {
      v = std::get<V>(elem);
    } else {
      for (const auto& [key, v_attr] : attributes_[kVertex]) {
        v_attr->IncrementSize();
      }
      position_.push_back(std::get<Vector3d>(elem));
      vStart_.push_back(kInvalidId);
    }
    for (const auto& [key, h_attr] : attributes_[kHalfedge]) {
      h_attr->IncrementSize();
    }
    hStart_.push_back(v);
    hCoStart_.push_back(vStart_.at(v));
    vStart_.at(v) = h;
  }
  return HFace(h_offset);
}
std::vector<V> Trimesh::RemoveFace(F f) {
  std::vector<V> removed_vertices;
  for (const auto& [key, f_attr] : attributes_[kFace]) {
    f_attr->ReplaceErase(f);
  }
  for (H h : std::views::reverse(FHalfedges(f))) {
    H g = hStart_.size() - 1;
    V v = hStart_[h];
    if (vStart_[v] == h) {
      vStart_[v] = hCoStart_[h];
    } else {
      for (H he : VStartings(v)) {
        if (hCoStart_[he] == h) {
          hCoStart_[he] = hCoStart_[h];
          break;
        }
      }
    }
    if (h != g) {
      V u = hStart_[g];
      hStart_[h] = u;
      hCoStart_[h] = hCoStart_[g];
      H* p = nullptr;
      if (vStart_[u] == g) {
        p = &vStart_[u];
      } else {
        for (H he : VStartings(u)) {
          if (hCoStart_[he] == g) {
            p = &hCoStart_[he];
            break;
          }
        }
      }
      *p = h;  // replace g with h and ensure the structure remains sorted
               // from greater to lower
      for (H nh = hCoStart_[h]; hCoStart_[h] > h && hCoStart_[h] != kInvalidId;
           nh = hCoStart_[h]) {
        *p = nh;
        hCoStart_[h] = hCoStart_[nh];
        hCoStart_[nh] = h;
        p = &hCoStart_[nh];
      }
    }
    hStart_.pop_back();
    hCoStart_.pop_back();
    for (const auto& [key, h_attr] : attributes_[kHalfedge]) {
      h_attr->ReplaceErase(h);
    }
    if (vStart_[v] == kInvalidId) {
      removed_vertices.push_back(v);
      for (H he : VStartings(vStart_.size() - 1)) {
        hStart_[he] = v;
      }
      vStart_[v] = vStart_.back(), vStart_.pop_back();
      position_[v] = std::move(position_.back()), position_.pop_back();
      for (const auto& [key, v_attr] : attributes_[kVertex]) {
        v_attr->ReplaceErase(v);
      }
    }
  }
  return removed_vertices;
}
std::vector<V> Trimesh::RemoveFaces(std::vector<F> faces) {
  std::ranges::sort(faces);
  const auto [first, last] = std::ranges::unique(faces);
  faces.erase(first, last);
  std::vector<V> removed_vertices;
  for (std::size_t i = 0; i < faces.size();) {
    F f = faces[i];
    std::vector<V> removed = RemoveFace(f);
    removed_vertices.insert(removed_vertices.end(), removed.begin(),
                            removed.end());
    if (faces.back() == NumFaces()) {
      faces.pop_back();
    } else {
      i++;
    }
  }
  return removed_vertices;
}
std::pair<std::vector<F>, std::vector<V>> Trimesh::CollapseEdge(H h) {
  std::vector<V> removed_vertices;
  std::vector<F> removed_faces = ToVector<F>(EdgeFaces(h));
  std::array<V, 2> verts = {HStart(h), HEnd(h)};
  Vector3d midpoint = (VPosition(verts[0]) + VPosition(verts[1])) / 2.0;
  V last_vert_id = NumVertices() - 1;
  for (size_t i = 0; i < removed_faces.size(); i++) {
    std::vector<V> rm_verts = RemoveFace(removed_faces[i]);
    removed_vertices.insert(removed_vertices.end(), rm_verts.begin(),
                            rm_verts.end());
    for (size_t j = i + 1; j < removed_faces.size(); j++) {
      if (removed_faces[j] == NumFaces()) {
        removed_faces[j] = removed_faces[i];
      }
    }
  }
  for (const V& rem_v : removed_vertices) {
    for (V& v : verts) {
      if (v == rem_v) {
        v = kInvalidId;
      } else if (v == last_vert_id) {
        v = rem_v;
      }
    }
    last_vert_id--;
  }
  if (verts[0] == kInvalidId) {
    std::swap(verts[0], verts[1]);
  }
  if (verts[0] == kInvalidId) {
    return std::make_pair(std::move(removed_faces),
                          std::move(removed_vertices));
  }
  position_[verts[0]] = midpoint;
  std::vector<H> v_starts;
  for (V vert : verts) {
    if (vert != kInvalidId) {
      for (H he : VStartings(vert)) {
        v_starts.push_back(he);
      }
    }
  }
  std::sort(v_starts.begin(), v_starts.end());
  vStart_[verts[0]] = kInvalidId;
  for (H he : v_starts) {
    hStart_[he] = verts[0];
    hCoStart_[he] = vStart_[verts[0]];
    vStart_[verts[0]] = he;
  }
  if (verts[1] != kInvalidId) {
    removed_vertices.push_back(verts[1]);
    if (verts[1] != vStart_.size() - 1) {
      for (H he : VStartings(vStart_.size() - 1)) {
        hStart_[he] = verts[1];
      }
      vStart_[verts[1]] = vStart_.back();
      position_[verts[1]] = std::move(position_.back());
    }
    vStart_.pop_back();
    position_.pop_back();
    for (const auto& [key, v_attr] : attributes_[kVertex]) {
      v_attr->ReplaceErase(verts[1]);
    }
  }
  return std::make_pair(std::move(removed_faces), std::move(removed_vertices));
}
void Trimesh::SplitEdge(H h) {
  std::variant<V, Vector3d> new_p = HCentroid(h);
  std::array<std::variant<V, Vector3d>, 3> tri;
  for (H he : ToVector<H>(EdgeHalfedges(h))) {
    tri = {new_p, HEnd(he), HStart(HPrev(he))};
    std::rotate(tri.begin(), tri.begin() + (3 - (he % 3)) % 3, tri.end());
    AddFace(tri);
    new_p = NumVertices() - 1;
    tri = {HStart(he), new_p, HStart(HPrev(he))};
    std::rotate(tri.begin(), tri.begin() + (3 - (he % 3)) % 3, tri.end());
    AddFace(tri);
    RemoveFace(HFace(he));
  }
}
void Trimesh::FlipHalfedgeWithOpposite(H h) {
  H hopp = HOpposite(h);
  if (hopp == kInvalidId) {
    throw std::invalid_argument("h param needs opposite to perform edge flip");
  }
  std::array<V, 4> verts{HStart(h), HEnd(h), HEnd(HNext(h)), HEnd(HNext(hopp))};
  if (verts[2] == verts[3]) {
    throw std::invalid_argument("Opp faces are identical, edge flip fails");
  }
  std::array<std::variant<V, Vector3d>, 3> tri = {verts[3], verts[2], verts[0]};
  std::rotate(tri.begin(), tri.begin() + (3 - (h % 3)) % 3, tri.end());
  AddFace(tri);
  RemoveFace(HFace(h));
  tri = {verts[2], verts[3], verts[1]};
  std::rotate(tri.begin(), tri.begin() + (3 - (hopp % 3)) % 3, tri.end());
  AddFace(tri);
  RemoveFace(HFace(hopp));
}
void Trimesh::DisconnectFace(F f) {
  AddFace({VPosition(HStart(3 * f)), VPosition(HStart(3 * f + 1)),
           VPosition(HStart(3 * f + 2))});
  RemoveFace(f);
}
void Trimesh::DisconnectFacesUntilManifoldEdges() {
  for (F f : std::views::reverse(Faces())) {
    for (H h : FHalfedges(f)) {
      if (!EdgeIsManifold(h)) {
        DisconnectFace(f);
        break;
      }
    }
  }
}
void Trimesh::DisconnectFacesUntilManifoldVertices() {
  std::queue<V> q;
  for (V v : Vertices()) {
    if (!VIsManifold(v)) {
      q.push(v);
    }
  }
  while (!q.empty()) {
    V v = q.front();
    q.pop();
    if (VIsManifold(v)) {
      continue;
    }
    std::unordered_set<V> s;
    for (H h : HConnectionsAroundStart(VStarting(v))) {
      s.insert(h);
    }
    for (H h : VStartings(v)) {
      if (!s.count(h)) {
        F f{HFace(h)};
        for (V u : FVertices(f)) {
          q.push(u);
        }
        DisconnectFace(f);
      }
    }
  }
}
void Trimesh::DisconnectFacesUntilManifold() {
  DisconnectFacesUntilManifoldEdges();
  DisconnectFacesUntilManifoldVertices();
}
template <MeshComponent C, typename T>
std::ranges::ref_view<std::vector<T>> Trimesh::CreateAttribute(
    const std::string& key) {
  if (attributes_[C].find(key) != attributes_[C].end()) {
    throw std::invalid_argument("Attribute already exists.");
  }
  size_t N = C == kHalfedge ? NumHalfedges()
             : C == kVertex ? NumVertices()
                            : NumFaces();
  attributes_[C][key] =
      std::make_unique<ContainerWrapper<std::vector<T>>>(std::vector<T>(N));
  return GetAttribute<C, T>(key);
}
template <MeshComponent C, typename T>
std::ranges::ref_view<std::vector<T>> Trimesh::GetAttribute(
    const std::string& key) {
  auto it = attributes_[C].find(key);
  if (it == attributes_[C].end()) {
    throw std::invalid_argument("Attribute does not exist.");
  }
  auto containerPtr =
      dynamic_cast<ContainerWrapper<std::vector<T>>*>(it->second.get());
  if (!containerPtr) {
    throw std::invalid_argument("Attribute exists but type does not match.");
  }
  return std::views::all(containerPtr->container_);
}
template <MeshComponent C>
void Trimesh::EraseAttribute(const std::string& key) {
  auto it = attributes_[C].find(key);
  if (it == attributes_[C].end()) {
    throw std::invalid_argument("Attribute does not exist.");
  }
  attributes_[C].erase(it);
}

}  // namespace TL

#endif  // TRILITE_TRIMESH_HPP
// MIT License
//
// Copyright (c) 2024 TriLite https://github.com/MeshLite/TriLite
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

#ifndef TRILITE_IO_HPP
#define TRILITE_IO_HPP

#include <fstream>
#include <iomanip>

namespace TL {

class IO {
 public:
  /**
   * @brief Determines the file format and calls the corresponding mesh reader
   * function.
   * @param filepath The path to the mesh file.
   * @return A Trimesh object representing the mesh.
   * @throws std::runtime_error if the file cannot be read or has an unsupported
   * format.
   */
  static Trimesh ReadMeshFile(const std::string& filepath);

  /**
   * @brief Writes a triangle mesh to a file, determining the appropriate format
   * from the file extension.
   * @param mesh The Trimesh object representing the mesh.
   * @param filepath The path to the output file.
   * @param binary_mode Whether the file must be written in binary mode (if
   * compatible with file extension).
   * @throws std::runtime_error if the file format is unsupported or if the file
   * cannot be opened for writing.
   */
  static void WriteMeshFile(const Trimesh& mesh, const std::string& filepath,
                            bool binary_mode = true);

 private:
  // Internal structures and functions
  static const int kAsciiDigitsPrecision_ = 10;
  struct Vector3Hash {
    std::size_t operator()(const Vector3d& key) const {
      const std::hash<double> hasher;
      size_t result = 0;
      for (int i = 0; i < 3; ++i) {
        result ^= hasher(key[i]) + 0x9e3779b9 + (result << 6) + (result >> 2);
      }
      return result;
    }
  };
  struct Float3Hash {
    std::size_t operator()(const std::array<float, 3>& key) const {
      const std::hash<float> hasher;
      size_t result = 0;
      for (int i = 0; i < 3; ++i) {
        result ^= hasher(key[i]) + 0x9e3779b9 + (result << 6) + (result >> 2);
      }
      return result;
    }
  };
  static std::vector<std::variant<V, Vector3d>> ConvertedToTrimeshPoints(
      const std::vector<Vector3d>& points) {
    std::vector<std::variant<V, Vector3d>> triangle_points;
    std::unordered_map<Vector3d, V, Vector3Hash> position_to_vertex;
    int n_duplicates = 0;
    for (size_t i = 0; i < points.size(); i += 3) {
      for (int j = 0; j < 3; j++) {
        auto [it, inserted] = position_to_vertex.emplace(
            points[i + j],
            static_cast<V>(position_to_vertex.size() + n_duplicates));
        for (int k = 0; k < j; k++) {
          if (points[i + j] == points[i + k]) {
            inserted = true;
            n_duplicates++;
            break;
          }
        }
        if (inserted) {
          triangle_points.push_back(points[i + j]);
        } else {
          triangle_points.push_back(it->second);
        }
      }
    }
    return triangle_points;
  }
  static std::vector<unsigned char> ReadBinaryFile(
      const std::string& filepath) {
    std::ifstream file(filepath, std::ios::binary | std::ios::ate);
    std::streamsize size = file.tellg();
    file.seekg(0, std::ios::beg);
    std::vector<unsigned char> buffer(size);
    file.read(reinterpret_cast<char*>(buffer.data()), size);
    return buffer;
  }
  static Trimesh ReadAsciiSTL(const std::string& filepath) {
    std::ifstream file(filepath);
    std::string line, token;
    std::vector<Vector3d> positions;
    Vector3d normal, vertex;
    while (std::getline(file, line)) {
      std::istringstream linestream(line);
      linestream >> token;
      if (token == "facet") {
        linestream >> token;
        linestream >> normal[0] >> normal[1] >> normal[2];
      } else if (token == "vertex") {
        linestream >> vertex[0] >> vertex[1] >> vertex[2];
        positions.push_back(vertex);
      } else if (token == "endfacet") {
        // Remove vertices if they don't count to three (error in file)
        positions.resize(positions.size() - (positions.size() % 3));
      }
    }
    positions.resize(positions.size() - (positions.size() % 3));
    return Trimesh(ConvertedToTrimeshPoints(positions));
  }
  static Trimesh ReadBinarySTL(const std::string& filepath) {
    const std::vector<unsigned char> binaryData = ReadBinaryFile(filepath);
    int nTriangles = *reinterpret_cast<const int*>(binaryData.data() + 80);
    std::vector<Vector3d> points(3 * nTriangles);
    float x;
    for (int i = 0; i < nTriangles; ++i) {
      auto ptr = binaryData.data() + 80 + 4 + 50 * i;
      for (int j : std::views::iota(1, 4)) {
        for (int k : std::views::iota(0, 3)) {
          memcpy(&x, ptr + j * 12 + k * 4, 4);
          points[3 * i + j - 1][k] = x;
        }
      }
    }
    return Trimesh(ConvertedToTrimeshPoints(points));
  }
  static Trimesh ReadSTL(const std::string& filepath) {
    std::ifstream file(filepath, std::ios::binary);
    char header[80];
    int nTriangles;
    file.read(header, 80);
    file.read(reinterpret_cast<char*>(&nTriangles), sizeof(nTriangles));
    file.seekg(0, std::ios::end);
    std::streampos fileSize = file.tellg();
    if (nTriangles * 50 + 84 == fileSize || strncmp(header, "solid", 5)) {
      return ReadBinarySTL(filepath);
    } else {
      return ReadAsciiSTL(filepath);
    }
  }
  static Trimesh ReadOBJ(const std::string& filepath) {
    std::ifstream file(filepath);
    std::string line;
    std::vector<Vector3d> points;
    std::vector<std::variant<V, Vector3d>> trimesh_points;
    std::vector<V> id_to_vid;
    Vector3d p;
    std::string s_index;
    V count_vids = 0;
    while (std::getline(file, line)) {
      std::istringstream lineStream(line);
      std::string lineType;
      lineStream >> lineType;
      if (lineType == "v") {
        lineStream >> p.x() >> p.y() >> p.z();
        points.push_back(std::move(p));
        id_to_vid.push_back({kInvalidId});
      } else if (lineType == "f") {
        std::vector<int> indices;
        while (lineStream >> s_index) {
          s_index = s_index.substr(0, s_index.find('/'));
          indices.push_back(std::stoi(s_index) - 1);
        }
        for (size_t i = 1; i < indices.size() - 1; ++i) {
          int idx[] = {indices[0], indices[i], indices[i + 1]};
          if (idx[0] == idx[1] || idx[0] == idx[2] || idx[1] == idx[2]) {
            continue;
          }
          for (int j : idx) {
            if (id_to_vid[j] != kInvalidId) {
              trimesh_points.push_back(id_to_vid[j]);
            } else {
              trimesh_points.push_back(points[j]);
              id_to_vid[j] = {count_vids++};
            }
          }
        }
      }
    }

    return Trimesh(trimesh_points);
  }
  static Trimesh ReadOFF(const std::string& filepath) {
    std::ifstream file(filepath);
    std::string line;
    std::getline(file, line);
    if (line != "OFF") {
      throw std::runtime_error("Invalid OFF file format");
    }
    int numVertices, numFaces, numEdges;
    file >> numVertices >> numFaces >> numEdges;
    std::vector<Vector3d> points(numVertices);
    std::vector<std::variant<V, Vector3d>> trimesh_points;
    std::vector<V> id_to_vid(numVertices, {kInvalidId});
    V count_vids = 0;
    for (Vector3d& p : points) {
      file >> p.x() >> p.y() >> p.z();
    }
    int numVerticesPerFace;
    for (int f = 0; f < numFaces; ++f) {
      file >> numVerticesPerFace;
      std::vector<int> indices(numVerticesPerFace);
      for (int& index : indices) {
        file >> index;
      }
      for (size_t i = 1; i < indices.size() - 1; ++i) {
        int idx[] = {indices[0], indices[i], indices[i + 1]};
        if (idx[0] == idx[1] || idx[0] == idx[2] || idx[1] == idx[2]) {
          continue;
        }
        for (int j : idx) {
          if (id_to_vid[j] != kInvalidId) {
            trimesh_points.push_back(id_to_vid[j]);
          } else {
            trimesh_points.push_back(points[j]);
            id_to_vid[j] = {count_vids++};
          }
        }
      }
    }
    return Trimesh(trimesh_points);
  }
  static Trimesh ReadBinaryPLY(const std::string& filepath) {
    std::ifstream file(filepath, std::ios::binary);
    std::string line;
    bool header_ended = false;
    int point_count = 0;
    int face_count = 0;
    bool is_big_endian = false;
    while (std::getline(file, line)) {
      std::istringstream iss(line);
      std::string token;
      iss >> token;
      if (line.find("binary_big_endian") != std::string::npos) {
        is_big_endian = true;
      } else if (token == "end_header") {
        header_ended = true;
        break;
      } else if (token == "element") {
        iss >> token;
        if (token == "vertex") {
          iss >> point_count;
        } else if (token == "face") {
          iss >> face_count;
        }
      }
    }
    if (!header_ended) {
      throw std::runtime_error("PLY end_header is missing.");
    }
    auto convert_endian = [](float& value) {
      char* value_ptr = reinterpret_cast<char*>(&value);
      std::reverse(value_ptr, value_ptr + sizeof(float));
    };
    std::vector<Vector3d> points(point_count);
    for (int i = 0; i < point_count; ++i) {
      std::array<float, 3> point;
      for (float& xyz : point) {
        file.read(reinterpret_cast<char*>(&xyz), sizeof(float));
        if (is_big_endian) {
          convert_endian(xyz);
        }
      }
      points[i] = Vector3d{point[0], point[1], point[2]};
    }
    V count_vids = 0;
    std::vector<V> id_to_vid(point_count, kInvalidId);
    std::vector<std::variant<V, Vector3d>> trimesh_points;
    for (int f = 0; f < face_count; ++f) {
      unsigned char vertex_count;
      file.read(reinterpret_cast<char*>(&vertex_count), sizeof(vertex_count));
      std::vector<int> indices(vertex_count);
      for (int j = 0; j < vertex_count; ++j) {
        int vertex_index;
        file.read(reinterpret_cast<char*>(&vertex_index), sizeof(vertex_index));
        indices[j] = vertex_index;
      }
      for (size_t i = 1; i < indices.size() - 1; ++i) {
        int idx[] = {indices[0], indices[i], indices[i + 1]};
        if (idx[0] == idx[1] || idx[0] == idx[2] || idx[1] == idx[2]) {
          continue;
        }
        for (int j : idx) {
          if (id_to_vid[j] != kInvalidId) {
            trimesh_points.push_back(id_to_vid[j]);
          } else {
            trimesh_points.push_back(points[j]);
            id_to_vid[j] = count_vids++;
          }
        }
      }
    }
    return Trimesh(trimesh_points);
  }
  static Trimesh ReadAsciiPLY(const std::string& filepath) {
    std::ifstream file(filepath);
    std::string line;
    bool header_ended = false;
    int point_count = 0;
    int face_count = 0;
    while (std::getline(file, line)) {
      std::istringstream iss(line);
      std::string token;
      iss >> token;
      if (token == "end_header") {
        header_ended = true;
        break;
      } else if (token == "element") {
        iss >> token;
        if (token == "vertex") {
          iss >> point_count;
        } else if (token == "face") {
          iss >> face_count;
        }
      }
    }
    if (!header_ended) {
      throw std::runtime_error("PLY end_header is missing.");
    }
    std::vector<Vector3d> points(point_count);
    for (Vector3d& p : points) {
      file >> p.x() >> p.y() >> p.z();
      file.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }
    std::vector<std::variant<V, Vector3d>> trimesh_points;
    std::vector<V> id_to_vid(point_count, kInvalidId);
    V count_vids = 0;
    for (int i = 0; i < face_count; ++i) {
      int vertex_count;
      file >> vertex_count;
      std::vector<int> indices(vertex_count);
      for (int& index : indices) {
        file >> index;
      }
      file.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
      for (size_t j = 1; j + 1 < indices.size(); ++j) {
        int idx[] = {indices[0], indices[j], indices[j + 1]};
        if (idx[0] == idx[1] || idx[0] == idx[2] || idx[1] == idx[2]) {
          continue;
        }
        for (int index : idx) {
          if (id_to_vid[index] != kInvalidId) {
            trimesh_points.push_back(id_to_vid[index]);
          } else {
            trimesh_points.push_back(points[index]);
            id_to_vid[index] = count_vids++;
          }
        }
      }
    }
    return Trimesh(trimesh_points);
  }
  static Trimesh ReadPLY(const std::string& filepath) {
    std::ifstream file(filepath, std::ios::binary);
    std::string line;
    getline(file, line);
    getline(file, line);
    file.close();
    if (line.find("ascii") != std::string::npos) {
      return ReadAsciiPLY(filepath);
    } else if (line.find("binary_little_endian") != std::string::npos) {
      return ReadBinaryPLY(filepath);
    } else if (line.find("binary_big_endian") != std::string::npos) {
      return ReadBinaryPLY(filepath);
    } else {
      throw std::runtime_error("Unsupported PLY format in file: " + filepath);
    }
  }
  static void WriteOBJ(const std::string& filepath, const Trimesh& mesh) {
    std::ofstream file(filepath);
    file << std::setprecision(kAsciiDigitsPrecision_);
    for (const auto& position : mesh.Positions()) {
      file << "v " << position.transpose() << '\n';
    }
    for (F f : mesh.Faces()) {
      file << "f";
      for (V v : mesh.FVertices(f)) {
        file << " " << v + 1;
      }
      file << '\n';
    }
    file.close();
  }
  static void WriteOFF(const std::string& filepath, const Trimesh& mesh) {
    std::ofstream file(filepath);
    file << std::setprecision(kAsciiDigitsPrecision_);
    file << "OFF\n" << mesh.NumVertices() << " " << mesh.NumFaces() << " 0\n";
    for (const auto& position : mesh.Positions()) {
      file << position.transpose() << '\n';
    }
    for (auto face : mesh.Faces()) {
      file << "3";
      for (V v : mesh.FVertices(face)) {
        file << " " << v;
      }
      file << '\n';
    }
    file.close();
  }
  static void WriteSTL(const std::string& filepath, const Trimesh& mesh,
                       bool binary_mode) {
    if (binary_mode) {
      std::unordered_map<std::array<float, 3>, V, Float3Hash> position_to_id;
      position_to_id.reserve(mesh.NumVertices());
      std::ofstream file(filepath, std::ios::binary);
      char header[80] = {};
      file.write(header, sizeof(header));
      uint32_t num_triangles = static_cast<uint32_t>(mesh.NumFaces());
      file.write(reinterpret_cast<const char*>(&num_triangles),
                 sizeof(num_triangles));
      auto write_float3 = [&file, &position_to_id](const Vector3d& vec,
                                                   V v = kInvalidId) {
        std::array<float, 3> data{static_cast<float>(vec[0]),
                                  static_cast<float>(vec[1]),
                                  static_cast<float>(vec[2])};
        if (v != kInvalidId) {
          // Displace the point until it is unique
          for (size_t i = 0;
               position_to_id.find(data) != position_to_id.end() &&
               position_to_id[data] != v;
               ++i) {
            if (!std::isfinite(data[i % 3])) {
              data[i % 3] = -std::numeric_limits<float>::infinity();
            }
            data[i % 3] = std::nextafter(
                data[i % 3], std::numeric_limits<float>::infinity());
          }
          position_to_id[data] = v;
        }
        file.write(reinterpret_cast<const char*>(&data), sizeof(data));
      };
      for (F f : mesh.Faces()) {
        write_float3(mesh.FNormal(f));
        for (V v : mesh.FVertices(f)) {
          write_float3(mesh.VPosition(v), v);
        }
        uint16_t attribute_byte_count = 0;
        file.write(reinterpret_cast<const char*>(&attribute_byte_count),
                   sizeof(attribute_byte_count));
      }
      file.close();
    } else {
      double increment = pow(10, 1 - kAsciiDigitsPrecision_);
      std::vector<Vector3d> positions{ToVector<Vector3d>(mesh.Positions())};
      std::vector<V> ids{ToVector<V>(mesh.Vertices())};
      std::sort(ids.begin(), ids.end(), [&positions](int u, int v) {
        return positions[u][0] < positions[v][0];
      });

      for (size_t i = 1; i < ids.size(); i++) {
        V u = ids[i - 1], v = ids[i];
        double ref =
            std::max(std::nextafter(positions[u][0],
                                    std::numeric_limits<double>::infinity()),
                     positions[u][0] + abs(positions[u][0]) * increment);
        positions[v][0] = std::max(positions[v][0], ref);
      }
      std::ofstream file(filepath);
      file << std::setprecision(kAsciiDigitsPrecision_) << "solid mesh\n";
      for (F f : mesh.Faces()) {
        file << "  facet normal " << mesh.FNormal(f).transpose() << "\n";
        file << "    outer loop\n";
        for (V v : mesh.FVertices(f)) {
          file << "    vertex " << positions[v].transpose() << "\n";
        }
        file << "    endloop\n";
        file << "  endfacet\n";
      }
      file << "endsolid mesh\n";
      file.close();
    }
  }
  static void WritePLY(const std::string& filepath, const Trimesh& mesh,
                       bool binary_mode) {
    std::ofstream file = binary_mode ? std::ofstream(filepath, std::ios::binary)
                                     : std::ofstream(filepath);
    if (!binary_mode) {
      file << std::setprecision(kAsciiDigitsPrecision_);
    }
    file << "ply\n";
    file << (binary_mode ? "format binary_little_endian 1.0\n"
                         : "format ascii 1.0\n");
    file << "element vertex " << mesh.NumVertices() << "\n";
    file << "property float x\n"
         << "property float y\n"
         << "property float z\n";
    file << "element face " << mesh.NumFaces() << "\n";
    file << "property list uchar int vertex_index\n";
    file << "end_header\n";
    for (const Vector3d& point : mesh.Positions()) {
      if (binary_mode) {
        for (float coord : point) {
          file.write(reinterpret_cast<const char*>(&coord), sizeof(float));
        }
      } else {
        file << point.transpose() << "\n";
      }
    }
    for (F f : mesh.Faces()) {
      unsigned char num_vertices = 3;
      if (binary_mode) {
        file.write(reinterpret_cast<const char*>(&num_vertices),
                   sizeof(num_vertices));
        for (V v : mesh.FVertices(f)) {
          file.write(reinterpret_cast<const char*>(&v), sizeof(v));
        }
      } else {
        file << 3 << " " << mesh.HStart(3 * f) << " " << mesh.HStart(3 * f + 1)
             << " " << mesh.HStart(3 * f + 2) << "\n";
      }
    }
    file.close();
  }
};

Trimesh IO::ReadMeshFile(const std::string& filepath) {
  std::ifstream file(filepath);
  if (!file.is_open()) {
    throw std::runtime_error("Could not open file for reading: " + filepath);
  }
  file.close();
  size_t dotPos = filepath.rfind('.');
  if (dotPos == std::string::npos) {
    throw std::runtime_error("No file extension found");
  }
  std::string extension = filepath.substr(dotPos + 1);
  std::transform(extension.begin(), extension.end(), extension.begin(),
                 [](unsigned char c) { return std::tolower(c); });
  if (extension == "stl") {
    return ReadSTL(filepath);
  } else if (extension == "obj") {
    return ReadOBJ(filepath);
  } else if (extension == "off") {
    return ReadOFF(filepath);
  } else if (extension == "ply") {
    return ReadPLY(filepath);
  } else {
    throw std::runtime_error("Unsupported file format: " + extension);
  }
}
void IO::WriteMeshFile(const Trimesh& mesh, const std::string& filepath,
                       bool binary_mode) {
  size_t dotPos = filepath.rfind('.');
  if (dotPos == std::string::npos) {
    throw std::runtime_error("No file extension found");
  }
  std::ofstream file(filepath);
  if (!file.is_open()) {
    throw std::runtime_error("Could not open file for writing: " + filepath);
  }
  file.close();
  std::string extension = filepath.substr(dotPos + 1);
  std::transform(extension.begin(), extension.end(), extension.begin(),
                 [](unsigned char c) { return std::tolower(c); });
  if (extension == "stl") {
    WriteSTL(filepath, mesh, binary_mode);
  } else if (extension == "obj") {
    WriteOBJ(filepath, mesh);
  } else if (extension == "off") {
    WriteOFF(filepath, mesh);
  } else if (extension == "ply") {
    WritePLY(filepath, mesh, binary_mode);
  } else {
    throw std::runtime_error("Unsupported file format: " + extension);
  }
}

}  // namespace TL

#endif  // TRILITE_IO_HPP
// The MIT License (MIT)
//
// Copyright (c) 2021 José Antonio Fernández Fernández
// Copyright (c) 2024 TriLite https://github.com/MeshLite/TriLite
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

#ifndef TRILITE_DISTANCE_HPP
#define TRILITE_DISTANCE_HPP

#include <algorithm>
#include <array>
#include <cmath>
#include <iostream>
#include <unordered_map>
#include <vector>

namespace TL {

class Distance {
 public:
  /**
   * @brief Computes the asymmetric Hausdorff distance between two triangle
   * meshes.
   *
   * This function computes the asymmetric Hausdorff distance between two
   * triangle meshes, `mesh` and `target_mesh`. The distance is calculated by
   * finding the maximum distance from any point on `mesh` to its closest point
   * on `target_mesh`.
   *
   * @param mesh The first triangle mesh from which points are sampled.
   * @param target_mesh The second triangle mesh to which distances are
   * calculated.
   * @param precision Desired precision for the computed asymmetric Hausdorff
   * distance, influencing the sampling density on the mesh.
   * @return double The computed asymmetric Hausdorff distance.
   */
  static double AsymmetricHausdorff(const Trimesh& mesh,
                                    const Trimesh& target_mesh,
                                    double precision);

  /**
   * @brief Computes the Hausdorff distance between two triangle meshes.
   *
   * This function computes the Hausdorff distance between two triangle meshes,
   * `mesh1` and `mesh2`. The distance is calculated as the maximum of the
   * asymmetric Hausdorff distances computed in both directions: from `mesh1`
   * to `mesh2` and from `mesh2` to `mesh1`.
   *
   * @param mesh1 The first triangle mesh.
   * @param mesh2 The second triangle mesh.
   * @param precision Desired precision for the computed Hausdorff distance,
   * influencing the sampling density on the mesh.
   * @return double The computed Hausdorff distance.
   */
  static double Hausdorff(const Trimesh& mesh1, const Trimesh& mesh2,
                          double precision);

  /**
   * @brief Computes the asymmetric mean Euclidean distance between two triangle
   * meshes.
   *
   * This function computes the asymmetric mean Euclidean distance between two
   * triangle meshes, `mesh1` and `mesh2`. The distance is calculated by
   * sampling points from `mesh` and finding the closest points on
   * `target_mesh`.
   *
   * @param mesh The first triangle mesh from which points are sampled.
   * @param target_mesh The second triangle mesh to which distances are
   * calculated.
   * @param precision Desired precision for the computed asymmetric mean
   * Euclidean distance, influencing the sampling density on the mesh.
   * @return double The computed asymmetric mean Euclidean distance.
   */
  static double AsymmetricMeanEuclidean(const Trimesh& mesh,
                                        const Trimesh& target_mesh,
                                        double precision);

  /**
   * @brief Computes the mean Euclidean distance between two triangle meshes.
   *
   * This function computes the mean Euclidean distance between two triangle
   * meshes, `mesh1` and `mesh2`. The distance is calculated by averaging the
   * asymmetric mean Euclidean distances computed in both directions: from
   * `mesh1` to `mesh2` and from `mesh2` to `mesh1`.
   *
   * @param mesh1 The first triangle mesh.
   * @param mesh2 The second triangle mesh.
   * @param precision Desired precision for the computed mean Euclidean
   * distance, influencing the sampling density on the mesh.
   * @return double The computed mean Euclidean distance.
   */
  static double MeanEuclidean(const Trimesh& mesh1, const Trimesh& mesh2,
                              double precision);

  class Tree {
   public:
    /**
     * @brief Constructs a Tree object with a given triangle mesh.
     *
     * Constructor that initializes the Tree object with a given triangle
     * mesh.
     *
     * @param mesh The triangle mesh used to construct the tree.
     */
    Tree(const Trimesh& mesh);

    /**
     * @brief Computes the unsigned Euclidean distance from a given point to
     * the nearest point on the mesh.
     *
     * This method computes the unsigned Euclidean distance from a given point
     * to the nearest point on the mesh.
     *
     * @param point The point from which the distance to the mesh is
     * calculated.
     * @return double The unsigned distance from the given point to the
     * closest point on the mesh.
     */
    double Distance(const Vector3d& point);

    /**
     * @brief Finds the closest point on the mesh to a given point.
     *
     * This method finds the closest point on the mesh to a given point.
     *
     * @param point The point from which the closest point on the mesh is
     * found.
     * @return Vector3d The closest point on the mesh to the given point.
     */
    Vector3d ClosestPoint(const Vector3d& point);

   private:
    // Point-Triangle distance declarations
    enum class NearestEntity { V0, V1, V2, E01, E12, E02, F };

    /**
     * Computes the squared distance, the nearest entity (vertex, edge or
     * face) and the nearest point from a point to a triangle.
     */
    static void PointTriangleSqUnsigned(double& distance_sq,
                                        NearestEntity& nearestEntity,
                                        Vector3d& barycentric,
                                        Vector3d& nearestPoint,
                                        const Vector3d& p, const Vector3d& a,
                                        const Vector3d& b, const Vector3d& c) {
      // This function is a modified version of the one found in the Real-Time
      // Collision Detection book by Ericson.
      Vector3d ab = b - a;
      Vector3d ac = c - a;
      Vector3d bc = c - b;

      // Compute parametric position s for projection P’ of P on AB
      double snom = (p - a).dot(ab), sdenom = (p - b).dot(a - b);
      // Compute parametric position t for projection P’ of P on AC
      double tnom = (p - a).dot(ac), tdenom = (p - c).dot(a - c);
      if (snom <= 0.0 && tnom <= 0.0) {
        nearestEntity = NearestEntity::V0;
        barycentric = {1.0, 0.0, 0.0};
        nearestPoint = a;
        distance_sq = (p - nearestPoint).squaredNorm();
        return;
      }

      // Compute parametric position u for projection P’ of P on BC
      double unom = (p - b).dot(bc), udenom = (p - c).dot(b - c);
      if (sdenom <= 0.0 && unom <= 0.0) {
        nearestEntity = NearestEntity::V1;
        barycentric = {0.0, 1.0, 0.0};
        nearestPoint = b;
        distance_sq = (p - nearestPoint).squaredNorm();
        return;
      }
      if (tdenom <= 0.0 && udenom <= 0.0) {
        nearestEntity = NearestEntity::V2;
        barycentric = {0.0, 0.0, 1.0};
        nearestPoint = c;
        distance_sq = (p - nearestPoint).squaredNorm();
        return;
      }

      // Normal for the triangle
      Vector3d n = ab.cross(ac);

      // Check if P is outside AB
      double vc = n.dot((a - p).cross(b - p));
      if (vc <= 0.0 && snom >= 0.0 && sdenom >= 0.0) {
        double arc = snom / (snom + sdenom);
        nearestEntity = NearestEntity::E01;
        barycentric = {1.0 - arc, arc, 0.0};
        nearestPoint = barycentric[0] * a + barycentric[1] * b;
        distance_sq = (p - nearestPoint).squaredNorm();
        return;
      }

      // Check if P is outside BC
      double va = n.dot((b - p).cross(c - p));
      if (va <= 0.0 && unom >= 0.0 && udenom >= 0.0) {
        double arc = unom / (unom + udenom);
        nearestEntity = NearestEntity::E12;
        barycentric = {0.0, 1.0 - arc, arc};
        nearestPoint = barycentric[1] * b + barycentric[2] * c;
        distance_sq = (p - nearestPoint).squaredNorm();
        return;
      }

      // Check if P is outside AC
      double vb = n.dot((c - p).cross(a - p));
      if (vb <= 0.0 && tnom >= 0.0 && tdenom >= 0.0) {
        double arc = tnom / (tnom + tdenom);
        nearestEntity = NearestEntity::E02;
        barycentric = {1.0 - arc, 0.0, arc};
        nearestPoint = barycentric[0] * a + barycentric[2] * c;
        distance_sq = (p - nearestPoint).squaredNorm();
        return;
      }

      // P must project inside the triangle; compute using barycentric
      // coordinates
      double u = va / (va + vb + vc);
      double v = vb / (va + vb + vc);
      double w = 1.0 - u - v;  // = vc / (va + vb + vc)
      nearestEntity = NearestEntity::F;
      barycentric = {u, v, w};
      nearestPoint = u * a + v * b + w * c;
      distance_sq = (p - nearestPoint).squaredNorm();
      return;
    }
    // -----------------------------------

    // Struct that contains the result of a distance query
    struct Result {
      double distance_ = std::numeric_limits<double>::max();
      Vector3d nearestPoint_;
      NearestEntity nearestEntity_;
      int triangleId_ = -1;
      Vector3d barycentric_;
    };
    struct BoundingSphere {
      Vector3d center_{0., 0., 0.};
      double radius_;
    };

    struct Node {
      BoundingSphere bvLeft_;
      BoundingSphere bvRight_;
      int left_ = -1;  // If left == -1, right is the triangle_id
      int right_ = -1;
    };

    struct Triangle {
      std::array<Vector3d, 3> vertices_;
      int id_ = -1;
    };

    std::vector<Vector3d> vertices_;
    std::vector<std::array<int, 3>> triangles_;
    std::vector<Node> nodes_;
    std::vector<Vector3d> pseudonormalsTriangles_;
    std::vector<std::array<Vector3d, 3>> pseudonormalsEdges_;
    std::vector<Vector3d> pseudonormalsVertices_;
    BoundingSphere rootBv_;
    bool isConstructed_ = false;

    void Construct();
    void BuildTree(const int node_id, BoundingSphere& bounding_sphere,
                   std::vector<Triangle>& triangles, const int begin,
                   const int end);
    void Query(Result& result, const Node& node, const Vector3d& point) const;

    Tree() = default;

    void Construct(const std::vector<Vector3d>& vertices,
                   const std::vector<std::array<int, 3>>& triangles);

    // Result signed_distance(const Vector3d& point) const;

    Result UnsignedResult(const Vector3d& point) const;
  };
};  // namespace

double Distance::AsymmetricHausdorff(const Trimesh& mesh,
                                     const Trimesh& target_mesh,
                                     double precision) {
  Tree tree(target_mesh);
  double hausdorff_d = 0;
  std::queue<std::pair<std::array<Vector3d, 3>, double>> q;
  for (F f : mesh.Faces()) {
    q.push(std::make_pair(
        std::array<Vector3d, 3>{mesh.VPosition(mesh.HStart(3 * f)),
                                mesh.VPosition(mesh.HStart(3 * f + 1)),
                                mesh.VPosition(mesh.HStart(3 * f + 2))},
        std::numeric_limits<double>::max()));
  }

  while (!q.empty()) {
    auto [tri, cur_max] = q.front();
    q.pop();
    if (cur_max < hausdorff_d + precision) {
      continue;
    }
    Vector3d bary = (tri[0] + tri[1] + tri[2]) / 3.;
    double bary_dist = tree.Distance(bary);
    hausdorff_d = std::max(hausdorff_d, bary_dist);
    double max_feasible =
        bary_dist + std::sqrt(std::max({(tri[0] - bary).squaredNorm(),
                                        (tri[1] - bary).squaredNorm(),
                                        (tri[2] - bary).squaredNorm()}));
    if (max_feasible > hausdorff_d + precision) {
      Vector3d a = (tri[0] + tri[1]) / 2.0;
      Vector3d b = (tri[1] + tri[2]) / 2.0;
      Vector3d c = (tri[2] + tri[0]) / 2.0;
      for (std::array<Vector3d, 3> sub_tri :
           std::array<std::array<Vector3d, 3>, 4>{
               std::array<Vector3d, 3>{a, b, c},
               std::array<Vector3d, 3>{tri[0], a, c},
               std::array<Vector3d, 3>{tri[1], b, a},
               std::array<Vector3d, 3>{tri[2], c, b}}) {
        q.push(std::make_pair(std::move(sub_tri), max_feasible));
      }
    }
  }
  return hausdorff_d;
}
double Distance::Hausdorff(const Trimesh& mesh1, const Trimesh& mesh2,
                           double precision) {
  return std::max(AsymmetricHausdorff(mesh1, mesh2, precision),
                  AsymmetricHausdorff(mesh2, mesh1, precision));
}
double Distance::AsymmetricMeanEuclidean(const Trimesh& mesh,
                                         const Trimesh& target_mesh,
                                         double precision) {
  // 18 / (2\sqrt{3} + \ln(\sqrt{3} + 2));
  const double ratio_precision_to_length = 3.764855876524;
  double distance = 0;
  double sum_area = 0;
  Tree distance_tree(target_mesh);
  double sq_length = pow(precision * ratio_precision_to_length, 2);
  std::function<void(std::array<Vector3d, 3>&&, double)> process_triangle =
      [&](std::array<Vector3d, 3>&& tri, double area) {
        if (std::max({(tri[1] - tri[0]).squaredNorm(),
                      (tri[2] - tri[1]).squaredNorm(),
                      (tri[0] - tri[2]).squaredNorm()}) <= sq_length) {
          distance +=
              area * distance_tree.Distance((tri[0] + tri[1] + tri[2]) / 3.0);
          return;
        }
        area /= 4.0;
        Vector3d a = (tri[0] + tri[1]) / 2.0;
        Vector3d b = (tri[1] + tri[2]) / 2.0;
        Vector3d c = (tri[2] + tri[0]) / 2.0;
        for (std::array<Vector3d, 3> sub_tri :
             std::array<std::array<Vector3d, 3>, 4>{
                 std::array<Vector3d, 3>{a, b, c},
                 std::array<Vector3d, 3>{tri[0], a, c},
                 std::array<Vector3d, 3>{tri[1], b, a},
                 std::array<Vector3d, 3>{tri[2], c, b}}) {
          process_triangle(std::move(sub_tri), area);
        }
      };

  for (TL::F f : mesh.Faces()) {
    std::array<Vector3d, 3> tri{mesh.VPosition(mesh.HStart(3 * f)),
                                mesh.VPosition(mesh.HStart(3 * f + 1)),
                                mesh.VPosition(mesh.HStart(3 * f + 2))};
    double area = mesh.FArea(f);
    process_triangle(std::move(tri), area);
    sum_area += area;
  }
  return distance / sum_area;
}
double Distance::MeanEuclidean(const Trimesh& mesh1, const Trimesh& mesh2,
                               double precision) {
  double distance1 = Distance::AsymmetricMeanEuclidean(mesh1, mesh2, precision);
  double distance2 = Distance::AsymmetricMeanEuclidean(mesh2, mesh1, precision);
  return (distance1 + distance2) / 2.0;
}
Distance::Tree::Tree(const Trimesh& mesh) {
  std::vector<Vector3d> vertices;
  for (const Vector3d& p : mesh.Positions()) {
    vertices.push_back({p[0], p[1], p[2]});
  }
  std::vector<std::array<int, 3>> triangles(mesh.NumFaces());
  for (F f : mesh.Faces()) {
    int i = 0;
    for (V v : mesh.FVertices(f)) {
      triangles[f][i++] = v;
    }
  }
  this->Construct(vertices, triangles);
}
double Distance::Tree::Distance(const Vector3d& point) {
  return UnsignedResult(point).distance_;
}
Vector3d Distance::Tree::ClosestPoint(const Vector3d& point) {
  Vector3d p = UnsignedResult(point).nearestPoint_;
  return {p[0], p[1], p[2]};
}
void Distance::Tree::Query(Result& result, const Node& node,
                           const Vector3d& point) const {
  // End of recursion
  if (node.left_ == -1) {
    const int triangle_id = node.right_;
    const std::array<int, 3>& triangle =
        this->triangles_[node.right_];  // If left == -1, right is the
                                        // triangle_id
    const Vector3d& v0 = this->vertices_[triangle[0]];
    const Vector3d& v1 = this->vertices_[triangle[1]];
    const Vector3d& v2 = this->vertices_[triangle[2]];

    double distance_sq;
    NearestEntity nearestEntity;
    Vector3d barycentric;
    Vector3d nearestPoint;
    PointTriangleSqUnsigned(distance_sq, nearestEntity, barycentric,
                            nearestPoint, point, v0, v1, v2);

    if (distance_sq < result.distance_ * result.distance_) {
      result.nearestEntity_ = nearestEntity;
      result.nearestPoint_ = nearestPoint;
      result.barycentric_ = barycentric;
      result.distance_ = std::sqrt(distance_sq);
      result.triangleId_ = triangle_id;
    }
  }

  // Recursion
  else {
    // Find which child bounding volume is closer
    const double d_left =
        (point - node.bvLeft_.center_).norm() - node.bvLeft_.radius_;
    const double d_right =
        (point - node.bvRight_.center_).norm() - node.bvRight_.radius_;

    if (d_left < d_right) {
      // Overlap test
      if (d_left < result.distance_) {
        this->Query(result, this->nodes_[node.left_], point);
      }

      if (d_right < result.distance_) {
        this->Query(result, this->nodes_[node.right_], point);
      }
    } else {
      if (d_right < result.distance_) {
        this->Query(result, this->nodes_[node.right_], point);
      }
      if (d_left < result.distance_) {
        this->Query(result, this->nodes_[node.left_], point);
      }
    }
  }
}
void Distance::Tree::Construct(
    const std::vector<Vector3d>& vertices,
    const std::vector<std::array<int, 3>>& triangles) {
  this->vertices_.resize(vertices.size());
  for (size_t i = 0; i < vertices.size(); i++) {
    this->vertices_[i][0] = (double)vertices[i][0];
    this->vertices_[i][1] = (double)vertices[i][1];
    this->vertices_[i][2] = (double)vertices[i][2];
  }
  this->triangles_.resize(triangles.size());
  for (size_t i = 0; i < triangles.size(); i++) {
    this->triangles_[i][0] = (int)triangles[i][0];
    this->triangles_[i][1] = (int)triangles[i][1];
    this->triangles_[i][2] = (int)triangles[i][2];
  }
  this->Construct();
}

// Result Tree::signed_distance(const Vector3d& point) const
// {
//   const Vector3d p(point[0], point[1], point[2]);
//   Result result = this->UnsignedResult(point);

//   const std::array<int, 3>& triangle =
//   this->triangles_[result.triangle_id]; Vector3d pseudonormal; switch
//   (result.nearestEntity) {
//     case NearestEntity::V0:
//       pseudonormal = this->pseudonormalsVertices[triangle[0]];
//       break;
//     case NearestEntity::V1:
//       pseudonormal = this->pseudonormalsVertices[triangle[1]];
//       break;
//     case NearestEntity::V2:
//       pseudonormal = this->pseudonormalsVertices[triangle[2]];
//       break;
//     case NearestEntity::E01:
//       pseudonormal = this->pseudonormalsEdges[result.triangle_id][0];
//       break;
//     case NearestEntity::E12:
//       pseudonormal = this->pseudonormalsEdges[result.triangle_id][1];
//       break;
//     case NearestEntity::E02:
//       pseudonormal = this->pseudonormalsEdges[result.triangle_id][2];
//       break;
//     case NearestEntity::F:
//       pseudonormal = this->pseudonormalsTriangles[result.triangle_id];
//       break;

//     default:
//       break;
//   }

//   const Vector3d nearestPoint(
//       result.barycentric[0] * this->vertices_[triangle[0]] +
//       result.barycentric[1] * this->vertices_[triangle[1]] +
//       result.barycentric[2] * this->vertices_[triangle[2]]);
//   const Vector3d u = p - nearestPoint;
//   result.distance_ *= (u.dot(pseudonormal) >= 0.0) ? 1.0 : -1.0;

//   return result;
// }

Distance::Tree::Result Distance::Tree::UnsignedResult(
    const Vector3d& point) const {
  if (!this->isConstructed_) {
    std::cout << "DistanceTriangleMesh error: not constructed." << std::endl;
    exit(-1);
  }

  const Vector3d p(point[0], point[1], point[2]);
  Result result;
  result.distance_ = std::numeric_limits<double>::max();
  this->Query(result, this->nodes_[0], p);
  return result;
}

void Distance::Tree::Construct() {
  if (this->triangles_.size() == 0) {
    std::cout << "DistanceTriangleMesh error: Empty triangle list."
              << std::endl;
    exit(-1);
  }

  // Build the tree containing the triangles
  std::vector<Triangle> triangles;

  triangles.resize(this->triangles_.size());
  for (int i = 0; i < (int)this->triangles_.size(); i++) {
    triangles[i].id_ = i;

    const std::array<int, 3>& triangle = this->triangles_[i];
    triangles[i].vertices_[0] = this->vertices_[triangle[0]];
    triangles[i].vertices_[1] = this->vertices_[triangle[1]];
    triangles[i].vertices_[2] = this->vertices_[triangle[2]];
  }

  this->nodes_.push_back(Node());
  this->BuildTree(0, this->rootBv_, triangles, 0, (int)triangles.size());

  // Compute pseudonormals
  //// Edge data structure
  std::unordered_map<uint64_t, Vector3d> edge_normals;
  std::unordered_map<uint64_t, int> edges_count;
  const uint64_t n_vertices = (uint64_t)this->vertices_.size();
  auto add_edge_normal = [&](const int i, const int j,
                             const Vector3d& triangle_normal) {
    const uint64_t key = std::min(i, j) * n_vertices + std::max(i, j);
    if (edge_normals.find(key) == edge_normals.end()) {
      edge_normals[key] = triangle_normal;
      edges_count[key] = 1;
    } else {
      edge_normals[key] += triangle_normal;
      edges_count[key] += 1;
    }
  };
  auto get_edge_normal = [&](const int i, const int j) {
    const uint64_t key = std::min(i, j) * n_vertices + std::max(i, j);
    return edge_normals.find(key)->second;
  };

  //// Compute
  this->pseudonormalsTriangles_.resize(this->triangles_.size());
  this->pseudonormalsEdges_.resize(this->triangles_.size());
  this->pseudonormalsVertices_.resize(this->vertices_.size(), {0, 0, 0});
  for (int i = 0; i < (int)this->triangles_.size(); i++) {
    // Triangle
    const std::array<int, 3>& triangle = this->triangles_[i];
    const Vector3d& a = this->vertices_[triangle[0]];
    const Vector3d& b = this->vertices_[triangle[1]];
    const Vector3d& c = this->vertices_[triangle[2]];

    const Vector3d triangle_normal = (b - a).cross(c - a).normalized();
    this->pseudonormalsTriangles_[i] = triangle_normal;

    // Vertex
    const double alpha_0 =
        std::acos((b - a).normalized().dot((c - a).normalized()));
    const double alpha_1 =
        std::acos((a - b).normalized().dot((c - b).normalized()));
    const double alpha_2 =
        std::acos((b - c).normalized().dot((a - c).normalized()));
    this->pseudonormalsVertices_[triangle[0]] += alpha_0 * triangle_normal;
    this->pseudonormalsVertices_[triangle[1]] += alpha_1 * triangle_normal;
    this->pseudonormalsVertices_[triangle[2]] += alpha_2 * triangle_normal;

    // Edge
    add_edge_normal(triangle[0], triangle[1], triangle_normal);
    add_edge_normal(triangle[1], triangle[2], triangle_normal);
    add_edge_normal(triangle[0], triangle[2], triangle_normal);
  }

  for (Vector3d& n : this->pseudonormalsVertices_) {
    n.normalize();
  }

  for (int tri_i = 0; tri_i < (int)this->triangles_.size(); tri_i++) {
    const std::array<int, 3>& triangle = this->triangles_[tri_i];
    this->pseudonormalsEdges_[tri_i][0] =
        get_edge_normal(triangle[0], triangle[1]).normalized();
    this->pseudonormalsEdges_[tri_i][1] =
        get_edge_normal(triangle[1], triangle[2]).normalized();
    this->pseudonormalsEdges_[tri_i][2] =
        get_edge_normal(triangle[0], triangle[2]).normalized();
  }

  this->isConstructed_ = true;
}

void Distance::Tree::BuildTree(const int node_id,
                               BoundingSphere& bounding_sphere,
                               std::vector<Triangle>& triangles,
                               const int begin, const int end) {
  const int n_triangles = end - begin;

  if (n_triangles == 0) {
    std::cout << "DistanceTriangleMesh::Construct error: Empty leave."
              << std::endl;
    exit(-1);
  } else if (n_triangles == 1) {
    // Build node leaf
    this->nodes_[node_id].left_ = -1;
    this->nodes_[node_id].right_ = triangles[begin].id_;

    //// Bounding sphere
    const Triangle& tri = triangles[begin];
    const Vector3d center =
        (tri.vertices_[0] + tri.vertices_[1] + tri.vertices_[2]) / 3.0;
    const double radius = std::max(std::max((tri.vertices_[0] - center).norm(),
                                            (tri.vertices_[1] - center).norm()),
                                   (tri.vertices_[2] - center).norm());
    bounding_sphere.center_ = center;
    bounding_sphere.radius_ = radius;
  } else {
    // Compute AxisAligned Bounding Box center and largest dimension of all
    // current triangles
    Vector3d top = {std::numeric_limits<double>::lowest(),
                    std::numeric_limits<double>::lowest(),
                    std::numeric_limits<double>::lowest()};
    Vector3d bottom = {std::numeric_limits<double>::max(),
                       std::numeric_limits<double>::max(),
                       std::numeric_limits<double>::max()};
    Vector3d center = {0, 0, 0};
    for (int tri_i = begin; tri_i < end; tri_i++) {
      for (int vertex_i = 0; vertex_i < 3; vertex_i++) {
        const Vector3d& p = triangles[tri_i].vertices_[vertex_i];
        center += p;

        for (int coord_i = 0; coord_i < 3; coord_i++) {
          top[coord_i] = std::max(top[coord_i], p[coord_i]);
          bottom[coord_i] = std::min(bottom[coord_i], p[coord_i]);
        }
      }
    }
    center /= 3 * n_triangles;
    const Vector3d diagonal = top - bottom;
    const int split_dim =
        (int)(std::max_element(&diagonal[0], &diagonal[0] + 3) - &diagonal[0]);

    // Set node bounding sphere
    double radius_sq = 0.0;
    for (int tri_i = begin; tri_i < end; tri_i++) {
      for (int i = 0; i < 3; i++) {
        radius_sq = std::max(
            radius_sq, (center - triangles[tri_i].vertices_[i]).squaredNorm());
      }
    }
    bounding_sphere.center_ = center;
    bounding_sphere.radius_ = std::sqrt(radius_sq);

    // Sort the triangles according to their center along the split
    // dimension
    std::sort(triangles.begin() + begin, triangles.begin() + end,
              [split_dim](const Triangle& a, const Triangle& b) {
                return a.vertices_[0][split_dim] < b.vertices_[0][split_dim];
              });

    // Children
    const int mid = (int)(0.5 * (begin + end));

    this->nodes_[node_id].left_ = (int)this->nodes_.size();
    this->nodes_.push_back(Node());
    this->BuildTree(this->nodes_[node_id].left_, this->nodes_[node_id].bvLeft_,
                    triangles, begin, mid);

    this->nodes_[node_id].right_ = (int)this->nodes_.size();
    this->nodes_.push_back(Node());
    this->BuildTree(this->nodes_[node_id].right_,
                    this->nodes_[node_id].bvRight_, triangles, mid, end);
  }
}
}  // namespace TL

#endif  // TRILITE_DISTANCE_HPP// MIT License
//
// Copyright (c) 2024 TriLite https://github.com/MeshLite/TriLite
// Copyright 2020 Tomas Akenine-Möller
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

#ifndef TRILITE_PROCESSING_HPP
#define TRILITE_PROCESSING_HPP

#include <set>

namespace TL {

class Processing {
 public:
  /**
   * @brief External decimation function to simplify a triangular mesh.
   * @param mesh Reference to the Trimesh object to be simplified.
   * @param target_face_count The target number of faces after decimation.
   */
  static void DecimateMesh(Trimesh& mesh, size_t target_face_count);

  /**
   * @brief Fills holes in a triangular mesh by detecting boundary edges and
   * adding triangles.
   * @param mesh The triangular mesh to be processed.
   */
  static void FillMeshHoles(Trimesh& mesh, size_t target_hole_count = 0);

  /**
   * @brief Applies volume-preserving Laplacian smoothing (Taubin smoothing) to
   * a triangular mesh.
   * @param mesh The triangular mesh to be smoothed.
   * @param iterations The number of smoothing iterations.
   * @param lambda The smoothing factor for the Laplacian step.
   * @param mu The inverse smoothing factor for the inverse Laplacian step.
   */
  static void TaubinSmoothing(Trimesh& mesh, int iterations = 1,
                              double lambda = 0.5, double mu = -0.53);

  /**
   * @brief Removes self-intersections from a triangular mesh.
   * @param mesh The triangular mesh to be processed.
   */
  static void RemoveSelfIntersections(Trimesh& mesh);

  /**
   * @brief Prepares a triangular mesh for 3D printing by iteratively closing it
   * while applying several cleaning and repair steps (only the largest
   * connected component is preserved).
   * @param mesh Reference to the Trimesh object to be prepared.
   * @param niters The number of iterations to perform (default is 10).
   */
  static void PrintabilityHeuristics(Trimesh& mesh, int niters = 10);

 private:
  static void ClampEdgeLengths(Trimesh& mesh, double min_length,
                               double max_length, int niters = 5) {
    for (int i = 0; i < niters; i++) {
      bool stop = true;
      for (H h : mesh.Halfedges()) {
        if (mesh.HLength(h) > max_length || mesh.HLength(h) < min_length) {
          stop = false;
          break;
        }
      }
      if (stop) {
        break;
      }
      F nf = mesh.NumFaces();
      std::vector<V> edge_to_v(mesh.NumHalfedges(), kInvalidId);
      std::vector<F> rm_faces;
      std::vector<std::vector<H>> edge_halfedges(mesh.NumHalfedges());
      for (H h : mesh.Halfedges()) {
        edge_halfedges[h] = ToVector<H>(mesh.EdgeHalfedges(h));
      }
      for (F f = 0; f < nf; f++) {
        int ct = 0;
        H he{kInvalidId};
        for (H h : mesh.FHalfedges(f)) {
          if (edge_to_v[h] != kInvalidId ||
              mesh.HLength(edge_halfedges[h].front()) > max_length) {
            ++ct;
            he = h;
          }
        }
        if (ct > 1) {
          rm_faces.push_back(f);
          std::vector<V> verts = {mesh.HStart(3 * f), mesh.HStart(3 * f + 1),
                                  mesh.HStart(3 * f + 2)};
          std::array<std::variant<V, Vector3d>, 3> centroids = {
              mesh.HCentroid(3 * f), mesh.HCentroid(3 * f + 1),
              mesh.HCentroid(3 * f + 2)};
          V num_v = mesh.NumVertices();
          for (int j : {0, 1, 2}) {
            if (edge_to_v[3 * f + j] != kInvalidId) {
              assert(edge_to_v[3 * f + j] < mesh.NumVertices());
              centroids[j] = edge_to_v[3 * f + j];
            } else {
              bool flag = false;
              for (H g : edge_halfedges[3 * f + j]) {
                flag |= (g == 3 * f + j);
                edge_to_v[g] = num_v;
              }
              assert(flag);
              ++num_v;
            }
          }
          mesh.AddFace(centroids);
          mesh.AddFace({verts[0], edge_to_v[3 * f], edge_to_v[3 * f + 2]});
          mesh.AddFace({verts[1], edge_to_v[3 * f + 1], edge_to_v[3 * f]});
          mesh.AddFace({verts[2], edge_to_v[3 * f + 2], edge_to_v[3 * f + 1]});
        } else if (ct == 1) {
          rm_faces.push_back(f);
          std::variant<V, Vector3d> centroid{mesh.HCentroid(he)};
          if (edge_to_v[he] != kInvalidId) {
            centroid = edge_to_v[he];
          } else {
            for (H g : edge_halfedges[he]) {  // mesh.EdgeHalfedges(he)) {
              edge_to_v[g] = mesh.NumVertices();
            }
          }
          mesh.AddFace(
              {mesh.HStart(mesh.HPrev(he)), mesh.HStart(he), centroid});
          centroid = edge_to_v[he];
          mesh.AddFace({mesh.HEnd(he), mesh.HStart(mesh.HPrev(he)), centroid});
        }
      }
      mesh.RemoveFaces(rm_faces);
      CollapseSmallEdges(mesh, min_length);
    }
  }
  static void CollapseSmallEdges(Trimesh& mesh, double min_length) {
    for (F f = 0; f < mesh.NumFaces();) {
      bool flag = true;
      for (H h : mesh.FHalfedges(f)) {
        if (mesh.HLength(h) < min_length) {
          mesh.CollapseEdge(h);
          flag = false;
          break;
        }
      }
      f += flag;
    }
  }
  static std::pair<TL::Vector3d, double> CalculateCircumsphere(
      const TL::Vector3d& a, const TL::Vector3d& b, const TL::Vector3d& c) {
    TL::Vector3d ac = c - a;
    TL::Vector3d ab = b - a;
    TL::Vector3d abxac = ab.cross(ac);

    TL::Vector3d to_circumsphere_center = (abxac.cross(ab) * ac.squaredNorm() +
                                           ac.cross(abxac) * ab.squaredNorm()) /
                                          (2.0 * abxac.squaredNorm());
    double circumsphere_radius = to_circumsphere_center.norm();
    TL::Vector3d ccs = a + to_circumsphere_center;

    return std::make_pair(ccs, circumsphere_radius);
  }
  static bool IsDelaunay(const TL::Trimesh& mesh, TL::H h) {
    TL::H hopp = mesh.HOpposite(h);
    if (hopp == TL::kInvalidId) {
      return true;
    }
    TL::Vector3d a = mesh.VPosition(mesh.HStart(h));
    TL::Vector3d b = mesh.VPosition(mesh.HEnd(h));
    TL::Vector3d c = mesh.VPosition(mesh.HEnd(mesh.HNext(h)));
    TL::Vector3d d = mesh.VPosition(mesh.HEnd(mesh.HNext(hopp)));
    std::pair<TL::Vector3d, double> sphere = CalculateCircumsphere(a, b, c);
    return (sphere.first - d).norm() >= (sphere.second);
  }
  static void MakeDelaunay(TL::Trimesh& mesh) {
    std::queue<TL::H> edge_queue;
    for (TL::H h : mesh.Halfedges()) {
      if (mesh.HOpposite(h) != TL::kInvalidId &&
          mesh.HOpposite(h) / 3 != mesh.HOpposite(mesh.HNext(h)) / 3) {
        edge_queue.push(h);
      }
    }
    size_t count = 0;
    size_t limit = 3 * mesh.NumFaces();
    while (!edge_queue.empty()) {
      if (count++ == limit) {
        break;
      }
      TL::H h = edge_queue.front();
      edge_queue.pop();
      TL::H hopp = mesh.HOpposite(h);
      if (hopp != TL::kInvalidId && !IsDelaunay(mesh, h)) {
        TL::V v1 = mesh.HStart(mesh.HPrev(h));
        TL::V v2 = mesh.HStart(mesh.HPrev(hopp));
        bool valid = true;
        for (TL::H he : mesh.VStartings(v1)) {
          valid &= (mesh.HEnd(he) != v2);
        }
        for (TL::H he : mesh.VStartings(v2)) {
          valid &= (mesh.HEnd(he) != v1);
        }
        if (valid) {
          mesh.FlipHalfedgeWithOpposite(h);
          edge_queue.push(mesh.HNext(h));
          edge_queue.push(mesh.HPrev(h));
          edge_queue.push(mesh.HNext(hopp));
          edge_queue.push(mesh.HPrev(hopp));
        }
      }
    }
  }
  static void RetainLargestComponent(TL::Trimesh& mesh) {
    std::vector<bool> visited(mesh.NumFaces(), false);
    std::vector<std::vector<F>> components;
    for (F f = 0; f < mesh.NumFaces(); ++f) {
      if (!visited[f]) {
        std::vector<F> component;
        std::vector<F> stack;
        stack.push_back(f);
        while (!stack.empty()) {
          F current = stack.back();
          stack.pop_back();
          if (visited[current]) continue;
          visited[current] = true;
          component.push_back(current);
          for (F neighbor : mesh.FNeighbors(current)) {
            if (!visited[neighbor]) {
              stack.push_back(neighbor);
            }
          }
        }
        components.push_back(component);
      }
    }
    size_t max_id = 0;
    for (size_t i = 1; i < components.size(); i++) {
      if (components[i].size() > components[max_id].size()) {
        max_id = i;
      }
    }
    std::vector<F> faces_to_delete;
    for (size_t i = 0; i < components.size(); i++) {
      if (i != max_id) {
        for (F f : components[i]) {
          faces_to_delete.push_back(f);
        }
      }
    }
    mesh.RemoveFaces(faces_to_delete);
  }

  struct BVHNode {
    Eigen::AlignedBox3d bbox_;
    std::optional<std::pair<TL::F, std::array<Vector3d, 3>>> triangle_;
    BVHNode* left_;
    BVHNode* right_;

    BVHNode() : left_(nullptr), right_(nullptr) {}
    ~BVHNode() {
      delete left_;
      delete right_;
    }
  };

  static BVHNode* ConstructBVH(
      std::vector<std::pair<TL::F, std::array<Vector3d, 3>>>& triangles,
      size_t start, size_t end, int depth = 0) {
    BVHNode* node = new BVHNode();
    assert(end > start);
    if (end - start == 1) {
      node->triangle_ = triangles[start];
      for (const auto& vertex : triangles[start].second) {
        node->bbox_.extend(vertex);
      }
    } else {
      for (size_t i = start; i < end; ++i) {
        for (const auto& vertex : triangles[i].second) {
          node->bbox_.extend(vertex);
        }
      }
      Vector3d extents = node->bbox_.sizes();
      int axis = 0;
      if (extents[1] > extents[0]) axis = 1;
      if (extents[2] > extents[axis]) axis = 2;
      std::sort(triangles.begin() + start, triangles.begin() + end,
                [axis](const std::pair<TL::F, std::array<Vector3d, 3>>& a,
                       const std::pair<TL::F, std::array<Vector3d, 3>>& b) {
                  return a.second[0][axis] < b.second[0][axis];
                });

      size_t mid = start + (end - start) / 2;
      node->left_ = ConstructBVH(triangles, start, mid, depth + 1);
      node->right_ = ConstructBVH(triangles, mid, end, depth + 1);
    }
    return node;
  }

  static bool DoesIntersect(
      BVHNode* node, const std::pair<TL::F, std::array<Vector3d, 3>>& tri) {
    if (!node || !node->bbox_.intersects(Eigen::AlignedBox3d(tri.second[0])
                                             .extend(tri.second[1])
                                             .extend(tri.second[2]))) {
      return false;
    }
    if (node->triangle_) {
      const auto& node_tri = node->triangle_.value();
      if (tri.first != node_tri.first &&
          Intersection::TriIntersectTri2(tri.second, node_tri.second)) {
        return true;
      }
    }
    return DoesIntersect(node->left_, tri) || DoesIntersect(node->right_, tri);
  }

  // Main function to find all auto-intersections in a mesh
  static std::vector<TL::F> FindSelfIntersections(TL::Trimesh& mesh,
                                                  double shrink_factor = 1e-8) {
    if (mesh.NumFaces() == 0) {
      return {};
    }
    std::vector<std::pair<TL::F, std::array<Vector3d, 3>>> triangles;
    for (TL::F f : mesh.Faces()) {
      if (mesh.FArea(f) > 1e-10) {
        Vector3d centroid = mesh.FCentroid(f);
        std::array<Vector3d, 3> tri;
        int i = 0;
        for (const Vector3d& position : mesh.FPositions(f)) {
          tri[i++] = position + (centroid - position) * shrink_factor;
        }
        triangles.emplace_back(f, tri);
      }
    }
    std::vector<TL::F> self_intersection_faces;
    BVHNode* bvh_root = ConstructBVH(triangles, 0, triangles.size());
    for (const auto& tri : triangles) {
      if (DoesIntersect(bvh_root, tri)) {
        self_intersection_faces.push_back(tri.first);
      }
    }
    delete bvh_root;
    return self_intersection_faces;
  }
  class Intersection {
   public:
    static bool TriIntersectTri2(std::array<Vector3d, 3> tri1,
                                 std::array<Vector3d, 3> tri2) {
      for (int i : {0, 1, 2}) {
        if (SegmentIntersectsTriangle({tri1[i], tri1[(i + 1) % 3]}, tri2)) {
          return true;
        }
        // if (SegmentIntersectsTriangle({tri2[i], tri2[(i + 1) % 3]}, tri1)) {
        //   return true;
        // }
      }
      return false;
    }

   private:
    // Function to check if a point is inside a triangle using barycentric
    // coordinates

    static bool SegmentIntersectsTriangle(const std::array<Vector3d, 2>& seg,
                                          const std::array<Vector3d, 3>& tri) {
      Vector3d N = (tri[1] - tri[0]).cross(tri[2] - tri[0]).normalized();
      Vector3d ray_vector = (seg[1] - seg[0]).normalized();
      Vector3d edge1 = tri[1] - tri[0];
      Vector3d edge2 = tri[2] - tri[0];
      Vector3d ray_cross_e2 = ray_vector.cross(edge2);
      double det = edge1.dot(ray_cross_e2);
      if (abs(det) < 1e-11) {
        // Edge is coplanar with the triangle
        if (std::abs((tri[0] - seg[0]).dot(N)) < 1e-11) {
          return CoplanarSegmentIntersectsTriangle(seg, tri);
        }
      } else {
        // Edge is not coplanar with the triangle
        return NoCoplanarSegmentIntersectsTriangle(seg, tri);
      }
      return false;
    }
    static bool NoCoplanarSegmentIntersectsTriangle(
        const std::array<Vector3d, 2>& seg,
        const std::array<Vector3d, 3>& tri) {
      Vector3d ray_origin = seg[0];
      Vector3d ray_vector = (seg[1] - seg[0]).normalized();
      Vector3d edge1 = tri[1] - tri[0];
      Vector3d edge2 = tri[2] - tri[0];
      Vector3d ray_cross_e2 = ray_vector.cross(edge2);
      double det = edge1.dot(ray_cross_e2);
      assert(abs(det) > 1e-12);
      double inv_det = 1.0 / det;
      Vector3d s = ray_origin - tri[0];
      double u = inv_det * s.dot(ray_cross_e2);
      if (u < 0.0 || u > 1.0) {
        return false;
      }
      Vector3d s_cross_e1 = s.cross(edge1);
      double v = inv_det * ray_vector.dot(s_cross_e1);
      if (v < 0.0 || u + v > 1.0) {
        return false;
      }
      double t = inv_det * edge2.dot(s_cross_e1);
      if (t >= 0.0 && t <= (seg[1] - seg[0]).norm()) {
        return true;
      } else {
        return false;
      }
    }
    static bool EdgeEdgeTest(const Vector3d& v0, const Vector3d& u0,
                             const Vector3d& u1, short i0, short i1, double ax,
                             double ay) {
      double bx = u0[i0] - u1[i0];
      double by = u0[i1] - u1[i1];
      double cx = v0[i0] - u0[i0];
      double cy = v0[i1] - u0[i1];
      double f = ay * bx - ax * by;
      double d = by * cx - bx * cy;
      if ((f > 0 && d >= 0 && d <= f) || (f < 0 && d <= 0 && d >= f)) {
        double e = ax * cy - ay * cx;
        if (f > 0) {
          if (e >= 0 && e <= f) return true;
        } else {
          if (e <= 0 && e >= f) return true;
        }
      }
      return false;
    }

    static bool EdgeAgainstTriEdges(const Vector3d& v0, const Vector3d& v1,
                                    const Vector3d& u0, const Vector3d& u1,
                                    const Vector3d& u2, short i0, short i1) {
      double ax = v1[i0] - v0[i0];
      double ay = v1[i1] - v0[i1];
      if (EdgeEdgeTest(v0, u0, u1, i0, i1, ax, ay)) {
        return true;
      }
      if (EdgeEdgeTest(v0, u1, u2, i0, i1, ax, ay)) {
        return true;
      }
      if (EdgeEdgeTest(v0, u2, u0, i0, i1, ax, ay)) {
        return true;
      }
      return false;
    }

    static bool CoplanarSegmentIntersectsTriangle(
        const std::array<Vector3d, 2>& seg,
        const std::array<Vector3d, 3>& tri) {
      short i0, i1;
      Vector3d edge = seg[1] - seg[0];
      Vector3d n = (tri[1] - tri[0]).cross(tri[2] - tri[0]);
      Vector3d a = n.cwiseAbs();
      if (a[0] > a[1]) {
        if (a[0] > a[2]) {
          i0 = 1;
          i1 = 2;
        } else {
          i0 = 0;
          i1 = 1;
        }
      } else {
        if (a[1] > a[2]) {
          i0 = 0;
          i1 = 2;
        } else {
          i0 = 0;
          i1 = 1;
        }
      }
      if (EdgeEdgeTest(seg[0], tri[0], tri[1], i0, i1, edge[i0], edge[i1])) {
        return true;
      }
      if (EdgeEdgeTest(seg[0], tri[1], tri[2], i0, i1, edge[i0], edge[i1])) {
        return true;
      }
      if (EdgeEdgeTest(seg[0], tri[2], tri[0], i0, i1, edge[i0], edge[i1])) {
        return true;
      }
      if (PointInTri(seg[0], tri[0], tri[1], tri[2], i0, i1)) {
        return true;
      }
      return false;
    }

    static bool PointInTri(const Vector3d& p, const Vector3d& u0,
                           const Vector3d& u1, const Vector3d& u2, short i0,
                           short i1) {
      double a, b, c, d0, d1, d2;
      a = u1[i1] - u0[i1];
      b = -(u1[i0] - u0[i0]);
      c = -a * u0[i0] - b * u0[i1];
      d0 = a * p[i0] + b * p[i1] + c;

      a = u2[i1] - u1[i1];
      b = -(u2[i0] - u1[i0]);
      c = -a * u1[i0] - b * u1[i1];
      d1 = a * p[i0] + b * p[i1] + c;

      a = u0[i1] - u2[i1];
      b = -(u0[i0] - u2[i0]);
      c = -a * u2[i0] - b * u2[i1];
      d2 = a * p[i0] + b * p[i1] + c;

      if (d0 * d1 > 0.0 && d0 * d2 > 0.0) {
        return true;
      }
      return false;
    }
  };
};

void Processing::DecimateMesh(Trimesh& mesh, size_t target_face_count) {
  std::vector<double> edge_lengths(mesh.NumHalfedges());
  auto compare = [&edge_lengths](H h, H g) {
    return edge_lengths[h] < edge_lengths[g] ||
           (edge_lengths[h] == edge_lengths[g] && h < g);
  };
  std::set<H, decltype(compare)> hset(compare);
  for (H h : mesh.Halfedges()) {
    edge_lengths[h] = mesh.HLength(h);
    assert(std::isfinite(edge_lengths[h]));
    hset.insert(h);
  }
  while (mesh.NumFaces() > target_face_count && !hset.empty()) {
    auto minh = *hset.begin();
    hset.erase(minh);
    if (minh >= mesh.NumHalfedges()) {
      continue;
    }
    std::array<V, 2> verts = {mesh.HStart(minh), mesh.HEnd(minh)};
    V last_vert_id = mesh.NumVertices() - 1;
    auto [rm_faces, rm_vertices] = mesh.CollapseEdge(minh);
    for (const V& rem_v : rm_vertices) {
      for (V& v : verts) {
        if (v == rem_v) {
          v = kInvalidId;
        } else if (v == last_vert_id) {
          v = rem_v;
        }
      }
      last_vert_id--;
    }
    for (F f : rm_faces) {
      for (H h : {3 * f, 3 * f + 1, 3 * f + 2}) {
        if (h < mesh.NumHalfedges()) {
          hset.erase(h);
        }
      }
    }
    for (V v : verts) {
      if (v != kInvalidId) {
        for (H h : mesh.VStartings(v)) {
          hset.erase(h);
        }
      }
    }
    for (F f : rm_faces) {
      for (H h : {3 * f, 3 * f + 1, 3 * f + 2}) {
        if (h < mesh.NumHalfedges()) {
          edge_lengths[h] = mesh.HLength(h);
          hset.insert(h);
        }
      }
    }
    for (V v : verts) {
      if (v != kInvalidId) {
        for (H h : mesh.VStartings(v)) {
          edge_lengths[h] = mesh.HLength(h);
          hset.insert(h);
        }
      }
    }
  }
}

void Processing::FillMeshHoles(Trimesh& mesh, size_t target_hole_count) {
  std::unordered_set<H> boundary_edges;
  std::vector<std::vector<H>> polygons;
  for (H st_h : mesh.BoundaryHalfedges()) {
    if (!boundary_edges.count(st_h)) {
      polygons.push_back(ToVector<H>(mesh.HHalfedgesAroundHole(st_h)));
      boundary_edges.insert(polygons.back().begin(), polygons.back().end());
    }
  }
  std::sort(polygons.begin(), polygons.end(),
            [](auto& A, auto& B) { return A.size() < B.size(); });
  size_t id = 0;
  for (const auto& polygon : polygons) {
    if (polygons.size() - id == target_hole_count) {
      break;
    }
    assert(polygon.size() >= 3);
    std::vector<double> sum_angle(polygon.size());
    auto set_sum_angle = [&mesh, &polygon, &sum_angle](size_t i) {
      H h = polygon[i];
      sum_angle[i] = 0;
      for (H he : mesh.HConnectionsAroundStart(h)) {
        sum_angle[i] += std::acos(
            std::clamp(mesh.HGeometry(he).normalized().dot(
                           -mesh.HGeometry(mesh.HPrev(he)).normalized()),
                       -1.0, 1.0));
      }
    };
    auto cmp = [&mesh, &sum_angle](std::pair<size_t, double> a,
                                   std::pair<size_t, double> b) {
      return a.second < b.second;
    };
    std::priority_queue<std::pair<size_t, double>,
                        std::vector<std::pair<size_t, double>>, decltype(cmp)>
        q(cmp);
    for (size_t i = 0; i < polygon.size(); i++) {
      set_sum_angle(i);
      q.push(std::make_pair(i, sum_angle[i]));
    }

    std::set<std::pair<size_t, H>> s;
    for (size_t i = 0; i < polygon.size(); i++) {
      s.insert(std::make_pair(i, polygon[i]));
    }
    while (!q.empty() && s.size() >= 3) {
      auto [i1, angle] = q.top();
      q.pop();
      if (angle != sum_angle[i1]) {
        continue;
      }
      H h1 = polygon[i1];
      auto it = s.find(std::make_pair(i1, h1));
      if (it == s.end()) {
        continue;
      }
      auto [i0, h0] = *((it == s.begin()) ? std::prev(s.end()) : std::prev(it));
      auto [i2, h2] = *((std::next(it) == s.end()) ? s.begin() : std::next(it));

      mesh.AddFace({mesh.HStart(h0), mesh.HStart(h2), mesh.HStart(h1)});
      sum_angle[i0] += std::acos(std::clamp(
          mesh.HGeometry(mesh.NumHalfedges() - 3)
              .normalized()
              .dot(-mesh.HGeometry(mesh.NumHalfedges() - 1).normalized()),
          -1.0, 1.0));
      q.push(std::make_pair(i0, sum_angle[i0]));
      sum_angle[i2] += std::acos(std::clamp(
          mesh.HGeometry(mesh.NumHalfedges() - 2)
              .normalized()
              .dot(-mesh.HGeometry(mesh.NumHalfedges() - 3).normalized()),
          -1.0, 1.0));
      q.push(std::make_pair(i2, sum_angle[i2]));
      s.erase(it);
    }
    id++;
  }
}

void Processing::TaubinSmoothing(Trimesh& mesh, int iterations, double lambda,
                                 double mu) {
  std::vector<Vector3d> new_positions(mesh.NumVertices());

  for (int iter = 0; iter < iterations; ++iter) {
    // Laplacian smoothing step (positive weight)
    for (V v : mesh.Vertices()) {
      Vector3d laplacian(0, 0, 0);
      size_t valence = 0;
      for (H h : mesh.VStartings(v)) {
        laplacian += mesh.VPosition(mesh.HEnd(h));
        ++valence;
      }
      laplacian /= static_cast<double>(valence);
      new_positions[v] =
          mesh.VPosition(v) + lambda * (laplacian - mesh.VPosition(v));
    }
    for (V v : mesh.Vertices()) {
      mesh.VPosition(v) = new_positions[v];
    }

    // Laplacian smoothing step (negative weight, inverse smoothing)
    for (V v : mesh.Vertices()) {
      Vector3d laplacian(0, 0, 0);
      size_t valence = 0;
      for (H h : mesh.VStartings(v)) {
        laplacian += mesh.VPosition(mesh.HEnd(h));
        ++valence;
      }
      laplacian /= static_cast<double>(valence);
      new_positions[v] =
          mesh.VPosition(v) + mu * (laplacian - mesh.VPosition(v));
    }
    for (V v : mesh.Vertices()) {
      mesh.VPosition(v) = new_positions[v];
    }
  }
}

void Processing::RemoveSelfIntersections(Trimesh& mesh) {
  std::vector<TL::F> rm_faces;
  for (TL::F f : FindSelfIntersections(mesh)) {
    rm_faces.push_back(f);
  }
  mesh.RemoveFaces(rm_faces);
}

void Processing::PrintabilityHeuristics(Trimesh& mesh, int niters) {
  if (mesh.NumFaces() == 0) {
    return;
  }
  RetainLargestComponent(mesh);
  std::vector<double> lengths(mesh.NumHalfedges());
  for (H h : mesh.Halfedges()) {
    lengths[h] = mesh.HLength(h);
  }
  std::sort(lengths.begin(), lengths.end());
  double max_length = 2.0 * lengths[lengths.size() / 2];
  double min_length = 0.5 * lengths[lengths.size() / 2];
  for (int i = 0; i < niters; i++) {
    ClampEdgeLengths(mesh, min_length, max_length);
    TL::Processing::RemoveSelfIntersections(mesh);
    mesh.DisconnectFacesUntilManifold();
    RetainLargestComponent(mesh);
    TL::Processing::FillMeshHoles(mesh, 0);
    mesh.DisconnectFacesUntilManifold();
    RetainLargestComponent(mesh);
    MakeDelaunay(mesh);
    TL::Processing::TaubinSmoothing(mesh);
  }
}
}  // namespace TL

#endif  // TRILITE_PROCESSING_HPP

#include <pybind11/eigen.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
namespace py = pybind11;
using namespace TL;

PYBIND11_MODULE(trilite, m) {
  py::class_<Trimesh>(m, "Trimesh")
      .def(py::init<>())
      .def(py::init<const std::vector<std::variant<V, Eigen::Vector3d>>&>())
      .def(py::init<const Trimesh&>())
      .def("NumHalfedges", &Trimesh::NumHalfedges)
      .def("NumVertices", &Trimesh::NumVertices)
      .def("NumFaces", &Trimesh::NumFaces)
      .def("Halfedges",
           [](const Trimesh& trimesh) {
             return TL::ToVector<H>(trimesh.Halfedges());
           })
      .def("Vertices",
           [](const Trimesh& trimesh) {
             return TL::ToVector<V>(trimesh.Vertices());
           })
      .def("Faces",
           [](const Trimesh& trimesh) {
             return TL::ToVector<F>(trimesh.Faces());
           })
      .def("Positions",
           [](const Trimesh& trimesh) {
             return TL::ToVector<Vector3d>(trimesh.Positions());
           })
      .def("HNext", &Trimesh::HNext)
      .def("HPrev", &Trimesh::HPrev)
      .def("HStart", &Trimesh::HStart)
      .def("HEnd", &Trimesh::HEnd)
      .def("HFace", &Trimesh::HFace)
      .def("HOpposite", &Trimesh::HOpposite)
      .def("HNextAroundStart", &Trimesh::HNextAroundStart)
      .def("HPrevAroundStart", &Trimesh::HPrevAroundStart)
      .def("HNextAroundEnd", &Trimesh::HNextAroundEnd)
      .def("HPrevAroundEnd", &Trimesh::HPrevAroundEnd)
      .def("HGeometry", &Trimesh::HGeometry)
      .def("HCentroid", &Trimesh::HCentroid)
      .def("HConnectionsAroundStart",
           [](const Trimesh& trimesh, H h) {
             return ToVector<H>(trimesh.HConnectionsAroundStart(h));
           })
      .def("HHalfedgesAroundHole",
           [](const Trimesh& trimesh, H h) {
             return ToVector<H>(trimesh.HHalfedgesAroundHole(h));
           })
      .def("HLength", &Trimesh::HLength)
      .def("VStarting", &Trimesh::VStarting)
      .def("VEnding", &Trimesh::VEnding)
      .def("VStartings", [](const Trimesh& trimesh,
                            V v) { return ToVector<H>(trimesh.VStartings(v)); })
      .def("VEndings", [](const Trimesh& trimesh,
                          V v) { return ToVector<H>(trimesh.VEndings(v)); })
      .def("VFaces", [](const Trimesh& trimesh,
                        V v) { return ToVector<F>(trimesh.VFaces(v)); })
      .def("VPosition", py::overload_cast<V>(&Trimesh::VPosition, py::const_))
      .def("VNormal", &Trimesh::VNormal)
      .def("VValence", &Trimesh::VValence)
      .def("VIsManifold", &Trimesh::VIsManifold)
      .def("FHalfedge", &Trimesh::FHalfedge)
      .def("FHalfedges", [](const Trimesh& trimesh,
                            F f) { return ToVector<H>(trimesh.FHalfedges(f)); })
      .def("FNeighbors", [](const Trimesh& trimesh,
                            F f) { return ToVector<H>(trimesh.FNeighbors(f)); })
      .def("FVertices", [](const Trimesh& trimesh,
                           F f) { return ToVector<V>(trimesh.FVertices(f)); })
      .def("FPositions",
           [](const Trimesh& trimesh, F f) {
             return ToVector<Vector3d>(trimesh.FPositions(f));
           })
      .def("FNormal", &Trimesh::FNormal)
      .def("FBoundingBox", &Trimesh::FBoundingBox)
      .def("FCentroid", &Trimesh::FCentroid)
      .def("FArea", &Trimesh::FArea)
      .def("EdgeHalfedges",
           [](const Trimesh& trimesh, H h) {
             return ToVector<H>(trimesh.EdgeHalfedges(h));
           })
      .def("EdgeFaces", [](const Trimesh& trimesh,
                           H h) { return ToVector<F>(trimesh.EdgeFaces(h)); })
      .def("EdgeIsManifold", &Trimesh::EdgeIsManifold)
      .def("BoundaryHalfedges",
           [](const Trimesh& trimesh) {
             return ToVector<H>(trimesh.BoundaryHalfedges());
           })
      .def("BoundingBox", &Trimesh::BoundingBox)
      .def("Centroid", &Trimesh::Centroid)
      .def("AddFace", &Trimesh::AddFace)
      .def("RemoveFace", &Trimesh::RemoveFace)
      .def("CollapseEdge", &Trimesh::CollapseEdge)
      .def("FlipHalfedgeWithOpposite", &Trimesh::FlipHalfedgeWithOpposite)
      .def("SplitEdge", &Trimesh::SplitEdge)
      .def("DisconnectFace", &Trimesh::DisconnectFace)
      .def("DisconnectFacesUntilManifoldEdges",
           &Trimesh::DisconnectFacesUntilManifoldEdges)
      .def("DisconnectFacesUntilManifoldVertices",
           &Trimesh::DisconnectFacesUntilManifoldVertices)
      .def("DisconnectFacesUntilManifold",
           &Trimesh::DisconnectFacesUntilManifold)
      .def("__copy__", [](const Trimesh& self) { return Trimesh(self); })
      .def("__deepcopy__",
           [](const Trimesh& self, py::dict) { return Trimesh(self); });

  py::class_<IO>(m, "IO")
      .def_static("ReadMeshFile", &IO::ReadMeshFile,
                  "Read a mesh file and return a Trimesh object",
                  py::arg("filepath"))
      .def_static("WriteMeshFile", &IO::WriteMeshFile,
                  "Write a Trimesh object to a mesh file", py::arg("mesh"),
                  py::arg("filepath"), py::arg("binary_mode") = true);

  py::class_<Processing>(m, "Processing")
      .def_static("DecimateMesh", &Processing::DecimateMesh,
                  "A function to simplify a triangular mesh", py::arg("mesh"),
                  py::arg("target_face_count"))
      .def_static("FillMeshHoles", &Processing::FillMeshHoles,
                  "A function to remove holes from triangular mesh",
                  py::arg("mesh"), py::arg("target_hole_count") = 0)
      .def_static("TaubinSmoothing", &Processing::TaubinSmoothing,
                  "Apply Laplacian smoothing to a mesh", py::arg("mesh"),
                  py::arg("iterations") = 1, py::arg("lambda") = 0.5,
                  py::arg("mu") = -0.53)
      .def_static(
          "RemoveSelfIntersections", &Processing::RemoveSelfIntersections,
          "A function to remove self-intersections in a triangular mesh",
          py::arg("mesh"))
      .def_static("PrintabilityHeuristics", &Processing::PrintabilityHeuristics,
                  "Prepares a triangular mesh for 3D printing by iteratively "
                  "closing it while applying several cleaning and repair steps "
                  "(only the largest connected component is preserved)",
                  py::arg("mesh"), py::arg("niters") = 10);

  py::class_<Distance>(m, "Distance")
      .def_static(
          "AsymmetricHausdorff", &Distance::AsymmetricHausdorff,
          "Compute the asymmetric Hausdorff distance between two meshes",
          py::arg("mesh"), py::arg("target_mesh"), py::arg("precision"))
      .def_static("Hausdorff", &Distance::Hausdorff,
                  "Compute the Hausdorff distance between two meshes",
                  py::arg("mesh1"), py::arg("mesh2"), py::arg("precision"))
      .def_static(
          "AsymmetricMeanEuclidean", &Distance::AsymmetricMeanEuclidean,
          "Compute the asymmetric mean Euclidean distance between two meshes",
          py::arg("mesh"), py::arg("target_mesh"), py::arg("precision"))
      .def_static("MeanEuclidean", &Distance::MeanEuclidean,
                  "Compute the mean Euclidean distance between two meshes",
                  py::arg("mesh1"), py::arg("mesh2"), py::arg("precision"));

  py::class_<Distance::Tree>(m.attr("Distance"), "Tree")
      .def(py::init<const Trimesh&>())
      .def("Distance", &Distance::Tree::Distance,
           "Compute the unsigned Euclidean distance from a point to the "
           "nearest point on the mesh",
           py::arg("point"))
      .def("ClosestPoint", &Distance::Tree::ClosestPoint,
           "Find the closest point on the mesh to a given point",
           py::arg("point"));
}