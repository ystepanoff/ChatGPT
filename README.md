# ChatGPT
# Note: this is now obsolete as ChatGPT got wrapped with Cloudflare. The future of this repo is unknown at the moment.
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/selenium?style=plastic) ![PyPI](https://img.shields.io/pypi/v/selenium?label=selenium&style=plastic) ![PyPI](https://img.shields.io/pypi/v/requests?label=requests&style=plastic) ![GitHub](https://img.shields.io/github/license/ystepanoff/ChatGPT?style=plastic)

Unofficial API wrapping for OpenAI ChatGPT: http://chat.openai.com/

# Example usage:
1. Clone the project.
2. Create virtual environment and install requirements.
3. Install Chrome binary and ChromeDriver.
4. 

```
$ python example.py --email <OpenAI e-mail> --password <OpenAI password> 
> Hello!
Hello! How can I help you today?
> Write Haskell code for the Ford-Fulkerson algorithm.
Here is an example implementation of the Ford-Fulkerson algorithm in Haskell:

import Data.Array
import Data.List
import qualified Data.Set as Set

-- The maximum flow in the given graph.
maxFlow :: Graph -> Int
maxFlow graph@(Graph _ _ s t) =
    let (_, flow) = maxFlowRecursive graph s t []
    in flow

-- Recursive function that computes the maximum flow in a given graph.
maxFlowRecursive :: Graph -> Vertex -> Vertex -> [Vertex] -> (Path, Int)
maxFlowRecursive graph@(Graph vertices edges _ _) source target visited =
    -- If we have reached the target, we are done.
    if source == target
        then ([], 0)
    else
        -- Otherwise, find the next edge to explore.
        let nextEdge = findEdge graph source visited
        in case nextEdge of
            -- If there are no more edges to explore, we are done.
            Nothing -> ([], 0)
            -- If there is an edge to explore, continue the search.
            Just (Edge u v capacity flow, remaining) ->
                let (path, flowDelta) = maxFlowRecursive graph v target (u:visited)
                in if flowDelta == 0
                    then ([], 0)
                    else (Edge u v capacity flow:path, flowDelta)

-- Finds the next edge to explore in the search for the maximum flow.
findEdge :: Graph -> Vertex -> [Vertex] -> Maybe (Edge, [Vertex])
findEdge (Graph vertices edges _ _) vertex visited =
    let availableEdges = filter (\(Edge u v _ _) -> u == vertex && not (v `elem` visited)) edges
    in case availableEdges of
        [] -> Nothing
        _ ->
            -- Select the edge with the minimum remaining capacity.
            let edge = minimumBy (\(Edge _ _ capacity1 _) (Edge _ _ capacity2 _) -> compare capacity1 capacity2) availableEdges
            in Just (edge, visited)

-- Represents a graph with vertices and edges.
data Graph = Graph {
    vertices :: Set.Set Vertex,
    edges :: [Edge],
    source :: Vertex,
    target :: Vertex
} deriving (Eq, Show)

-- Represents an edge in the graph.
data Edge = Edge {
    u :: Vertex,
    v :: Vertex,
    capacity :: Int,
    flow :: Int
} deriving (Eq, Show)

-- Represents a vertex in the graph.
type Vertex = Int


To use this code, you will need to create a `Graph` object with the desired vertices and edges, and then call `maxFlow` on the `Graph` to compute the maximum flow. For example:

let graph = Graph (Set.fromList [1, 2, 3, 4, 5]) [Edge 1 2 10 0, Edge 1 3 5 0, Edge 2 3 2 0, Edge 2 4 4 0, Edge 3 5 10 0, Edge 4 5 10 0] 1 5
let maxFlow = maxFlow graph

This code assumes that the vertices are represented using integers, and that the edges are represented using the `Edge` data type defined above. You can modify the code as needed to suit your specific
>
```
