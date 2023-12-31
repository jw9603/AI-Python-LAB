import torch
import networkx as nx
import numpy as np



def find_cycles(edge_index):
    num_nodes = max(edge_index.max().item(), edge_index.max().item()) + 1

    adj_list = {i: [] for i in range(num_nodes)}
    for i, j in edge_index.T.tolist():
        adj_list[i].append(j)

    def find_cycles_dfs(node, start_node, depth, visited, path, cycles):
        visited[node] = True
        path.append(node)

        if depth == 2:
            if start_node in adj_list[node]:
                cycle = list(path)
                min_idx = cycle.index(min(cycle))
                cycle = cycle[min_idx:] + cycle[:min_idx]
                cycles.add(tuple(cycle))
        elif depth <= 2:
            for neighbor in adj_list[node]:
                if not visited[neighbor]:
                    find_cycles_dfs(neighbor, start_node, depth + 1, visited, path, cycles)

        path.pop()
        visited[node] = False

    cycles = set()
    for start_node in range(num_nodes):
        visited = [False] * num_nodes
        find_cycles_dfs(start_node, start_node, 0, visited, [], cycles)

    node_list = [list(cycle) for cycle in cycles]
    return node_list


if __name__ =='__main__':
    
   edge_index = torch.tensor([[  4,   4,   4,   4,   4,   6,   6,  11,  14,  15,  15,  15,  15,  19,
          19,  24,  24,  26,  26,  26,  26,  31,  32,  38,  38,  39,  39,  48,
          48,  48,  49,  50,  53,  56,  56,  58,  62,  65,  71,  72,  72,  74,
          74,  76,  80,  82,  85,  95,  97,  97, 100,   2,   2,   2,   2,   2,
           2,   6,   7,   7,  14,  14,  14,  14,  15,  15,  15,  24,  24,  26,
          26,  26,  26,  29,  30,  31,  32,  38,  42,  46,  49,  59,  61,  61,
          61,  64,  76,  89,  94,  33,  75,  89,  90,   1,   2,   2,   3,   4,
          15,  15,  19,  26,  26,  26,  29,  31,  32,  32,  38,  40,  47,  50,
          51,  54,  55,  55,  57,  63,  67,  67,  71,  73,  77,  81,  83,  89,
          89,  90,  94,   4,   4,   4,   6,  13,  22,  28,  32,  39,  40,  44,
          48,  67,  72,  80,  80,  90,  93, 100,  14,  56,  69,  75,   2,   6,
           7,  19,  24,  32,  33,  38,  24,  31,  38,  72,   6,  24,  24,  33,
          83,  94,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
           1,   1,   1,   2,   2,   2,   2,   2,   3,   4,   4,   4,   4,   4,
           4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
           4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   5,   5,
           5,   5,   5,   5,   5,   6,   6,   6,   6,   6,   6,   6,   6,   6,
           6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,
           6,   6,   6,   7,   7,   8,   8,   9,   9,   9,  10,  10,  10,  11,
          11,  12,  12,  12,  13,  13,  13,  13,  14,  14,  14,  14,  14,  15,
          15,  15,  15,  15,  15,  15,  15,  15,  15,  15,  15,  15,  15,  15,
          15,  15,  15,  15,  15,  15,  16,  16,  16,  17,  18,  18,  18,  18,
          18,  18,  18,  18,  18,  18,  19,  19,  19,  19,  19,  19,  19,  19,
          19,  19,  20,  20,  21,  21,  21,  21,  21,  21,  22,  24,  24,  24,
          24,  24,  24,  24,  24,  24,  24,  24,  24,  24,  24,  25,  25,  25,
          26,  26,  26,  26,  26,  26,  26,  26,  26,  26,  26,  26,  26,  26,
          26,  26,  27,  28,  28,  28,  28,  29,  29,  29,  29,  29,  29,  29,
          29,  29,  29,  30,  30,  30,  30,  30,  30,  31,  31,  31,  31,  31,
          31,  31,  32,  32,  32,  32,  32,  32,  32,  33,  34,  34,  34,  34,
          34,  35,  35,  35,  36,  36,  36,  36,  36,  36,  36,  36,  36,  37,
          37,  37,  37,  37,  37,  37,  37,  37,  37,  37,  37,  37,  38,  38,
          38,  38,  38,  38,  38,  38,  39,  39,  39,  39,  39,  39,  39,  39,
          39,  39,  39,  39,  40,  40,  42,  42,  42,  42,  42,  42,  42,  42,
          43,  43,  43,  43,  44,  44,  44,  44,  44,  45,  45,  45,  45,  45,
          46,  46,  46,  46,  46,  46,  46,  46,  47,  47,  47,  47,  47,  48,
          48,  48,  48,  49,  49,  49,  49,  49,  49,  49,  49,  49,  49,  50,
          50,  50,  50,  50,  50,  50,  50,  50,  50,  51,  51,  51,  51,  51,
          52,  52,  53,  54,  54,  54,  54,  55,  55,  56,  56,  56,  56,  56,
          58,  58,  58,  58,  58,  58,  59,  59,  59,  59,  59,  59,  59,  59,
          59,  59,  59,  59,  59,  59,  60,  60,  60,  60,  60,  60,  60,  60,
          61,  61,  62,  62,  62,  62,  63,  63,  63,  63,  63,  63,  63,  63,
          64,  64,  64,  64,  64,  64,  64,  64,  65,  67,  67,  67,  67,  67,
          68,  68,  68,  68,  68,  68,  68,  69,  69,  69,  69,  70,  70,  70,
          70,  71,  71,  71,  71,  71,  71,  71,  71,  71,  72,  72,  72,  72,
          72,  72,  72,  72,  72,  72,  72,  72,  73,  73,  73,  73,  73,  73,
          74,  74,  74,  74,  74,  74,  74,  74,  74,  75,  75,  76,  76,  76,
          76,  76,  76,  76,  76,  76,  76,  77,  77,  77,  77,  79,  79,  79,
          79,  80,  80,  80,  80,  80,  80,  80,  80,  80,  80,  80,  80,  80,
          80,  80,  80,  82,  82,  82,  82,  82,  82,  82,  82,  82,  82,  83,
          83,  83,  83,  83,  83,  83,  83,  83,  84,  84,  84,  84,  84,  84,
          84,  86,  86,  87,  87,  87,  87,  87,  87,  87,  87,  88,  89,  89,
          89,  89,  89,  89,  89,  89,  90,  90,  90,  90,  91,  91,  91,  91,
          91,  91,  91,  92,  92,  93,  93,  94,  95,  95,  95,  97,  98,  98,
          98,  99, 100, 100, 100,   6,  26,  61,  61,  73,  86,  89,   0,   0,
           0,   0,   0,   0,   0,  48,  52,  73,  85,  92,  15,  26,  97,  32,
           2,   6,  14,  26,   6,  38,  19,  58,   6,  14,  15,  38,  58,  14,
           6,  26,  14,  31,   4,   5,  70,  71,  63,  65,  47,  64,  31,  38,
          53,  49,  44,  53,  48,  92,  49,  66,  31,   5,  92,   5,  11,  80,
          31,  39,  42,  45,  71,  82,  76,  45,  46,  24,  46,  71,  76,  32,
          39,  71,  56,  71,  14,  39,  45,  46,  71,  59,  82,  39,  31,  39,
          76,  46,  71,   2,  39,  58,  91,  46,  64,  58,   4,  62,  77,   4,
          76,  36,  86,  47,  62,  28,  39,  86,   6,  25,  86,  26,  58,  36,
          86,  86,  62,  63,   3,  40,  26,  47,  73,  84,  49,  16,  51,  49,
          47,  64,   3,  68,  40,  51,  61,  24,  40,  62,  74,  77,  66,  62,
          62,  39,  66,  62,  62,  62,   4,  43,  44,  62,   4,   4,  92,  76,
          64,  36,  71,  96,  96,  25,  96,  96,   2,  25,  96,  15,  19,  19,
          19,  35,   5,  88,   5,   5,   5,  14,  23,  31,  41,  43,  47,  49,
          53,  56,  63,  66,  71,  75,  76,  78,  15,  32,  39,  65,  86,  47,
           5,  16,  17,  22,  23,  24,  27,  30,  33,  37,  40,  41,  44,  50,
          51,  57,  59,  61,  62,  63,  67,  70,  73,  74,  78,  79,  85,  88,
          95,  99, 101,   4,  11,  34,  70,  88,  98, 101,   2,  13,  14,  15,
          24,  25,  26,  28,  32,  34,  39,  53,  57,  58,  60,  65,  73,  75,
          76,  77,  81,  84,  86,  87,  92,  94,  26,  84,   3,   6,   4,   5,
          34,   3,   4,  47,   4,   5,   4,   5,  88,   7,  64,  66,  77,  24,
          41,  64,  76,  81,   2,   3,   6,   7,  14,  24,  26,  28,  29,  31,
          32,  34,  35,  38,  39,  47,  57,  65,  81,  82,  86,   4,   5,  67,
           3,   2,   6,  14,  26,  39,  58,  64,  65,  76, 100,   3,  25,  31,
          38,  47,  57,  65,  72,  81,  86,   4,   5,   5,   6,  25,  49,  65,
          71,   3,   5,   6,  14,  15,  25,  39,  47,  56,  57,  58,  81,  86,
          94,  96,   6,  26,  57,   2,   6,   7,  14,  25,  29,  32,  34,  38,
          39,  42,  53,  56,  57,  65,  86,   5,   3,  47,  50,  57,   2,   6,
           7,  26,  39,  49,  55,  57,  65,  82,   2,  28,  57,  75,  77,  86,
          19,  25,  32,  39,  47,  58,  86,   2,  14,  26,  39,  53,  57,  75,
          37,   5,  15,  25,  35,  38,   5,  34,  55,   3,  38,  47,  55,  57,
          65,  69,  81,  92,   3,   4,   5,  25,  47,  57,  64,  67,  70,  72,
          73,  86,  91,   3,  19,  26,  47,  56,  57,  73,  86,   2,   7,  14,
          25,  31,  32,  42,  45,  57,  63,  64,  65,   5,  51,   2,   5,  32,
          39,  45,  57,  65,  82,   4,  45,  62,  68,   4,   6,  28,  62,  80,
           2,  39,  43,  53,  57,   3,   4,  14,  49,  50,  63,  76,  92,   3,
          63,  65,  69,  73,   4,   5,  50,  79,   2,  29,  34,  39,  47,  53,
          57,  63,  65,  71,   1,   6,  23,  41,  47,  56,  57,  63,  65,  72,
           5,  37,  40,  64,  89,   5,  48,  75,   5,   6,  21,  49,   4,   5,
           1,   3,  47,  57,  64,   7,  14,  31,  47,  50,  57,   3,   6,  15,
          19,  42,  47,  53,  57,  61,  63,  68,  72,  76,  86,   2,   6,  15,
          25,  39,  42,  47,  65,  39,  48,   4,   5,  38,  65,  36,  39,  41,
          47,  49,  50,  92,  97,   1,   3,  14,  33,  37,  47,  53,  86,  53,
           4,   5,  26,  37,  55,   4,   5,   9,  41,  45,  57,  83,   1,   3,
          47,  57,   4,   5,  98, 101,   1,  49,  53,  57,  58,  63,  65,  75,
          76,   5,   6,   7,  19,  25,  39,  47,  50,  53,  57,  65,  73,   3,
           5,  38,  47,  55,  65,   4,   5,   6,   7,  40,  41,  44,  95, 101,
          23,  36,  14,  46,  49,  53,  56,  57,  63,  64,  65,  82,   4,  39,
          57,  81,   5,  24,  51,  65,   3,   5,  14,  24,  25,  31,  39,  44,
          47,  50,  57,  65,  66,  73,  81, 100,   6,  15,  19,  25,  47,  53,
          57,  58,  73,  81,   4,   5,  26,  57,  63,  65,  68,  72,  75,   7,
          26,  39,  63,  65,  81,  87,  57,  81,   6,   7,  45,  56,  57,  61,
          65,  84,   5,   4,   5,  40,  51,  61,  64,  65,  79,   4,   5,  14,
          61,   2,   6,  32,  39,  61,  64,  82,  36,  47,   5,   6,  24,   5,
          40,  74,   4,   3,  70, 101,   5,   6,   7,  44,  66,  29,   2,  14,
          48,  81,  51,   1,   2,   3,   4,   5,   6,   7],
        [ 48,  52,  73,  85,  92,  15,  26,  97,  32,   2,   6,  14,  26,   6,
          38,  19,  58,   6,  14,  15,  38,  58,  14,   6,  26,  14,  31,   4,
           5,  70,  71,  63,  65,  47,  64,  31,  38,  53,  49,  44,  53,  48,
          92,  49,  66,  31,   5,  92,   5,  11,  80,  31,  39,  42,  45,  71,
          82,  76,  45,  46,  24,  46,  71,  76,  32,  39,  71,  56,  71,  14,
          39,  45,  46,  71,  59,  82,  39,  31,  39,  76,  46,  71,   2,  39,
          58,  91,  46,  64,  58,   4,  62,  77,   4,  76,  36,  86,  47,  62,
          28,  39,  86,   6,  25,  86,  26,  58,  36,  86,  86,  62,  63,   3,
          40,  26,  47,  73,  84,  49,  16,  51,  49,  47,  64,   3,  68,  40,
          51,  61,  24,  40,  62,  74,  77,  66,  62,  62,  39,  66,  62,  62,
          62,   4,  43,  44,  62,   4,   4,  92,  76,  64,  36,  71,  96,  96,
          25,  96,  96,   2,  25,  96,  15,  19,  19,  19,  35,   5,  88,   5,
           5,   5,  14,  23,  31,  41,  43,  47,  49,  53,  56,  63,  66,  71,
          75,  76,  78,  15,  32,  39,  65,  86,  47,   5,  16,  17,  22,  23,
          24,  27,  30,  33,  37,  40,  41,  44,  50,  51,  57,  59,  61,  62,
          63,  67,  70,  73,  74,  78,  79,  85,  88,  95,  99, 101,   4,  11,
          34,  70,  88,  98, 101,   2,  13,  14,  15,  24,  25,  26,  28,  32,
          34,  39,  53,  57,  58,  60,  65,  73,  75,  76,  77,  81,  84,  86,
          87,  92,  94,  26,  84,   3,   6,   4,   5,  34,   3,   4,  47,   4,
           5,   4,   5,  88,   7,  64,  66,  77,  24,  41,  64,  76,  81,   2,
           3,   6,   7,  14,  24,  26,  28,  29,  31,  32,  34,  35,  38,  39,
          47,  57,  65,  81,  82,  86,   4,   5,  67,   3,   2,   6,  14,  26,
          39,  58,  64,  65,  76, 100,   3,  25,  31,  38,  47,  57,  65,  72,
          81,  86,   4,   5,   5,   6,  25,  49,  65,  71,   3,   5,   6,  14,
          15,  25,  39,  47,  56,  57,  58,  81,  86,  94,  96,   6,  26,  57,
           2,   6,   7,  14,  25,  29,  32,  34,  38,  39,  42,  53,  56,  57,
          65,  86,   5,   3,  47,  50,  57,   2,   6,   7,  26,  39,  49,  55,
          57,  65,  82,   2,  28,  57,  75,  77,  86,  19,  25,  32,  39,  47,
          58,  86,   2,  14,  26,  39,  53,  57,  75,  37,   5,  15,  25,  35,
          38,   5,  34,  55,   3,  38,  47,  55,  57,  65,  69,  81,  92,   3,
           4,   5,  25,  47,  57,  64,  67,  70,  72,  73,  86,  91,   3,  19,
          26,  47,  56,  57,  73,  86,   2,   7,  14,  25,  31,  32,  42,  45,
          57,  63,  64,  65,   5,  51,   2,   5,  32,  39,  45,  57,  65,  82,
           4,  45,  62,  68,   4,   6,  28,  62,  80,   2,  39,  43,  53,  57,
           3,   4,  14,  49,  50,  63,  76,  92,   3,  63,  65,  69,  73,   4,
           5,  50,  79,   2,  29,  34,  39,  47,  53,  57,  63,  65,  71,   1,
           6,  23,  41,  47,  56,  57,  63,  65,  72,   5,  37,  40,  64,  89,
           5,  48,  75,   5,   6,  21,  49,   4,   5,   1,   3,  47,  57,  64,
           7,  14,  31,  47,  50,  57,   3,   6,  15,  19,  42,  47,  53,  57,
          61,  63,  68,  72,  76,  86,   2,   6,  15,  25,  39,  42,  47,  65,
          39,  48,   4,   5,  38,  65,  36,  39,  41,  47,  49,  50,  92,  97,
           1,   3,  14,  33,  37,  47,  53,  86,  53,   4,   5,  26,  37,  55,
           4,   5,   9,  41,  45,  57,  83,   1,   3,  47,  57,   4,   5,  98,
         101,   1,  49,  53,  57,  58,  63,  65,  75,  76,   5,   6,   7,  19,
          25,  39,  47,  50,  53,  57,  65,  73,   3,   5,  38,  47,  55,  65,
           4,   5,   6,   7,  40,  41,  44,  95, 101,  23,  36,  14,  46,  49,
          53,  56,  57,  63,  64,  65,  82,   4,  39,  57,  81,   5,  24,  51,
          65,   3,   5,  14,  24,  25,  31,  39,  44,  47,  50,  57,  65,  66,
          73,  81, 100,   6,  15,  19,  25,  47,  53,  57,  58,  73,  81,   4,
           5,  26,  57,  63,  65,  68,  72,  75,   7,  26,  39,  63,  65,  81,
          87,  57,  81,   6,   7,  45,  56,  57,  61,  65,  84,   5,   4,   5,
          40,  51,  61,  64,  65,  79,   4,   5,  14,  61,   2,   6,  32,  39,
          61,  64,  82,  36,  47,   5,   6,  24,   5,  40,  74,   4,   3,  70,
         101,   5,   6,   7,  44,  66,  29,   2,  14,  48,  81,  51,   1,   2,
           3,   4,   5,   6,   7,   4,   4,   4,   4,   4,   6,   6,  11,  14,
          15,  15,  15,  15,  19,  19,  24,  24,  26,  26,  26,  26,  31,  32,
          38,  38,  39,  39,  48,  48,  48,  49,  50,  53,  56,  56,  58,  62,
          65,  71,  72,  72,  74,  74,  76,  80,  82,  85,  95,  97,  97, 100,
           2,   2,   2,   2,   2,   2,   6,   7,   7,  14,  14,  14,  14,  15,
          15,  15,  24,  24,  26,  26,  26,  26,  29,  30,  31,  32,  38,  42,
          46,  49,  59,  61,  61,  61,  64,  76,  89,  94,  33,  75,  89,  90,
           1,   2,   2,   3,   4,  15,  15,  19,  26,  26,  26,  29,  31,  32,
          32,  38,  40,  47,  50,  51,  54,  55,  55,  57,  63,  67,  67,  71,
          73,  77,  81,  83,  89,  89,  90,  94,   4,   4,   4,   6,  13,  22,
          28,  32,  39,  40,  44,  48,  67,  72,  80,  80,  90,  93, 100,  14,
          56,  69,  75,   2,   6,   7,  19,  24,  32,  33,  38,  24,  31,  38,
          72,   6,  24,  24,  33,  83,  94,   1,   1,   1,   1,   1,   1,   1,
           1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   3,
           4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
           4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
           4,   4,   4,   5,   5,   5,   5,   5,   5,   5,   6,   6,   6,   6,
           6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,
           6,   6,   6,   6,   6,   6,   6,   6,   7,   7,   8,   8,   9,   9,
           9,  10,  10,  10,  11,  11,  12,  12,  12,  13,  13,  13,  13,  14,
          14,  14,  14,  14,  15,  15,  15,  15,  15,  15,  15,  15,  15,  15,
          15,  15,  15,  15,  15,  15,  15,  15,  15,  15,  15,  16,  16,  16,
          17,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  19,  19,  19,
          19,  19,  19,  19,  19,  19,  19,  20,  20,  21,  21,  21,  21,  21,
          21,  22,  24,  24,  24,  24,  24,  24,  24,  24,  24,  24,  24,  24,
          24,  24,  25,  25,  25,  26,  26,  26,  26,  26,  26,  26,  26,  26,
          26,  26,  26,  26,  26,  26,  26,  27,  28,  28,  28,  28,  29,  29,
          29,  29,  29,  29,  29,  29,  29,  29,  30,  30,  30,  30,  30,  30,
          31,  31,  31,  31,  31,  31,  31,  32,  32,  32,  32,  32,  32,  32,
          33,  34,  34,  34,  34,  34,  35,  35,  35,  36,  36,  36,  36,  36,
          36,  36,  36,  36,  37,  37,  37,  37,  37,  37,  37,  37,  37,  37,
          37,  37,  37,  38,  38,  38,  38,  38,  38,  38,  38,  39,  39,  39,
          39,  39,  39,  39,  39,  39,  39,  39,  39,  40,  40,  42,  42,  42,
          42,  42,  42,  42,  42,  43,  43,  43,  43,  44,  44,  44,  44,  44,
          45,  45,  45,  45,  45,  46,  46,  46,  46,  46,  46,  46,  46,  47,
          47,  47,  47,  47,  48,  48,  48,  48,  49,  49,  49,  49,  49,  49,
          49,  49,  49,  49,  50,  50,  50,  50,  50,  50,  50,  50,  50,  50,
          51,  51,  51,  51,  51,  52,  52,  53,  54,  54,  54,  54,  55,  55,
          56,  56,  56,  56,  56,  58,  58,  58,  58,  58,  58,  59,  59,  59,
          59,  59,  59,  59,  59,  59,  59,  59,  59,  59,  59,  60,  60,  60,
          60,  60,  60,  60,  60,  61,  61,  62,  62,  62,  62,  63,  63,  63,
          63,  63,  63,  63,  63,  64,  64,  64,  64,  64,  64,  64,  64,  65,
          67,  67,  67,  67,  67,  68,  68,  68,  68,  68,  68,  68,  69,  69,
          69,  69,  70,  70,  70,  70,  71,  71,  71,  71,  71,  71,  71,  71,
          71,  72,  72,  72,  72,  72,  72,  72,  72,  72,  72,  72,  72,  73,
          73,  73,  73,  73,  73,  74,  74,  74,  74,  74,  74,  74,  74,  74,
          75,  75,  76,  76,  76,  76,  76,  76,  76,  76,  76,  76,  77,  77,
          77,  77,  79,  79,  79,  79,  80,  80,  80,  80,  80,  80,  80,  80,
          80,  80,  80,  80,  80,  80,  80,  80,  82,  82,  82,  82,  82,  82,
          82,  82,  82,  82,  83,  83,  83,  83,  83,  83,  83,  83,  83,  84,
          84,  84,  84,  84,  84,  84,  86,  86,  87,  87,  87,  87,  87,  87,
          87,  87,  88,  89,  89,  89,  89,  89,  89,  89,  89,  90,  90,  90,
          90,  91,  91,  91,  91,  91,  91,  91,  92,  92,  93,  93,  94,  95,
          95,  95,  97,  98,  98,  98,  99, 100, 100, 100,   6,  26,  61,  61,
          73,  86,  89,   0,   0,   0,   0,   0,   0,   0]])
   edge_type = torch.tensor([ 2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,
         2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,
         2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  3,  3,  3,
         3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,
         3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  4,
         4,  4,  5,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
         7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
         7,  7,  7,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,
         9,  9,  9,  9, 10, 10, 10, 10, 12, 12, 12, 12, 12, 12, 12, 12, 13, 13,
        13, 13, 16, 16, 16, 16, 16, 16, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
        17, 17, 17, 17, 17, 17, 17, 17, 17, 18, 18, 18, 18, 18, 18, 18,  0,  0,
         0,  1,  1,  1,  1, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
        21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
        21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
        21, 21, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
        22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
        22, 22, 22, 22, 23, 23, 23, 24, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26,
        26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26,
        26, 26, 26, 26, 26, 26, 26, 26, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28,
        28, 28, 28, 28, 28, 28, 28, 28, 28, 29, 29, 29, 29, 31, 31, 31, 31, 31,
        31, 31, 31, 32, 32, 32, 32, 35, 35, 35, 35, 35, 35, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
        36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 37, 37, 37, 37,
        37, 37, 37, 19, 19, 19, 20, 20, 20, 20])
   print(find_cycles(edge_index))
    