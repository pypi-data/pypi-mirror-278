


example = {
  "nftables": [
    {
      "metainfo": {
        "version": "1.0.2",
        "release_name": "Lester Gooch",
        "json_schema_version": 1
      }
    },
    {
      "table": {
        "family": "inet",
        "name": "filter",
        "handle": 23
      }
    },
    {
      "chain": {
        "family": "inet",
        "table": "filter",
        "name": "input",
        "handle": 1,
        "type": "filter",
        "hook": "input",
        "prio": 0,
        "policy": "accept"
      }
    },
    {
      "chain": {
        "family": "inet",
        "table": "filter",
        "name": "forward",
        "handle": 2,
        "type": "filter",
        "hook": "forward",
        "prio": 0,
        "policy": "accept"
      }
    },
    {
      "chain": {
        "family": "inet",
        "table": "filter",
        "name": "output",
        "handle": 3,
        "type": "filter",
        "hook": "output",
        "prio": 0,
        "policy": "accept"
      }
    },
    {
      "table": {
        "family": "ip",
        "name": "nat",
        "handle": 24
      }
    },
    {
      "chain": {
        "family": "ip",
        "table": "nat",
        "name": "DOCKER",
        "handle": 1
      }
    },
    {
      "rule": {
        "family": "ip",
        "table": "nat",
        "chain": "DOCKER",
        "handle": 10,
        "expr": [
          {
            "match": {
              "op": "==",
              "left": {
                "meta": {
                  "key": "iifname"
                }
              },
              "right": "docker0"
            }
          },
          {
            "counter": {
              "packets": 0,
              "bytes": 0
            }
          },
          {
            "return": None
          }
        ]
      }
    },
    {
      "chain": {
        "family": "ip",
        "table": "nat",
        "name": "POSTROUTING",
        "handle": 2,
        "type": "nat",
        "hook": "postrouting",
        "prio": 100,
        "policy": "accept"
      }
    },
    {
      "rule": {
        "family": "ip",
        "table": "nat",
        "chain": "POSTROUTING",
        "handle": 9,
        "expr": [
          {
            "match": {
              "op": "!=",
              "left": {
                "meta": {
                  "key": "oifname"
                }
              },
              "right": "docker0"
            }
          },
          {
            "match": {
              "op": "==",
              "left": {
                "payload": {
                  "protocol": "ip",
                  "field": "saddr"
                }
              },
              "right": {
                "prefix": {
                  "addr": "172.17.0.0",
                  "len": 16
                }
              }
            }
          },
          {
            "counter": {
              "packets": 4,
              "bytes": 286
            }
          },
          {
            "xt": None
          }
        ]
      }
    },
    {
      "chain": {
        "family": "ip",
        "table": "nat",
        "name": "PREROUTING",
        "handle": 5,
        "type": "nat",
        "hook": "prerouting",
        "prio": -100,
        "policy": "accept"
      }
    },
    {
      "rule": {
        "family": "ip",
        "table": "nat",
        "chain": "PREROUTING",
        "handle": 6,
        "expr": [
          {
            "xt": None
          },
          {
            "counter": {
              "packets": 2,
              "bytes": 168
            }
          },
          {
            "jump": {
              "target": "DOCKER"
            }
          }
        ]
      }
    },
    {
      "chain": {
        "family": "ip",
        "table": "nat",
        "name": "OUTPUT",
        "handle": 7,
        "type": "nat",
        "hook": "output",
        "prio": -100,
        "policy": "accept"
      }
    },
    {
      "rule": {
        "family": "ip",
        "table": "nat",
        "chain": "OUTPUT",
        "handle": 8,
        "expr": [
          {
            "match": {
              "op": "!=",
              "left": {
                "payload": {
                  "protocol": "ip",
                  "field": "daddr"
                }
              },
              "right": {
                "prefix": {
                  "addr": "127.0.0.0",
                  "len": 8
                }
              }
            }
          },
          {
            "xt": None
          },
          {
            "counter": {
              "packets": 0,
              "bytes": 0
            }
          },
          {
            "jump": {
              "target": "DOCKER"
            }
          }
        ]
      }
    },
    {
      "table": {
        "family": "ip",
        "name": "filter",
        "handle": 25
      }
    },
    {
      "chain": {
        "family": "ip",
        "table": "filter",
        "name": "DOCKER",
        "handle": 1
      }
    },
    {
      "chain": {
        "family": "ip",
        "table": "filter",
        "name": "DOCKER-ISOLATION-STAGE-1",
        "handle": 2
      }
    },
    {
      "rule": {
        "family": "ip",
        "table": "filter",
        "chain": "DOCKER-ISOLATION-STAGE-1",
        "handle": 19,
        "expr": [
          {
            "match": {
              "op": "==",
              "left": {
                "meta": {
                  "key": "iifname"
                }
              },
              "right": "docker0"
            }
          },
          {
            "match": {
              "op": "!=",
              "left": {
                "meta": {
                  "key": "oifname"
                }
              },
              "right": "docker0"
            }
          },
          {
            "counter": {
              "packets": 6,
              "bytes": 426
            }
          },
          {
            "jump": {
              "target": "DOCKER-ISOLATION-STAGE-2"
            }
          }
        ]
      }
    },
    {
      "rule": {
        "family": "ip",
        "table": "filter",
        "chain": "DOCKER-ISOLATION-STAGE-1",
        "handle": 4,
        "expr": [
          {
            "counter": {
              "packets": 12,
              "bytes": 974
            }
          },
          {
            "return": None
          }
        ]
      }
    },
    {
      "chain": {
        "family": "ip",
        "table": "filter",
        "name": "DOCKER-ISOLATION-STAGE-2",
        "handle": 3
      }
    },
    {
      "rule": {
        "family": "ip",
        "table": "filter",
        "chain": "DOCKER-ISOLATION-STAGE-2",
        "handle": 20,
        "expr": [
          {
            "match": {
              "op": "==",
              "left": {
                "meta": {
                  "key": "oifname"
                }
              },
              "right": "docker0"
            }
          },
          {
            "counter": {
              "packets": 0,
              "bytes": 0
            }
          },
          {
            "drop": None
          }
        ]
      }
    },
    {
      "rule": {
        "family": "ip",
        "table": "filter",
        "chain": "DOCKER-ISOLATION-STAGE-2",
        "handle": 5,
        "expr": [
          {
            "counter": {
              "packets": 6,
              "bytes": 426
            }
          },
          {
            "return": None
          }
        ]
      }
    },
    {
      "chain": {
        "family": "ip",
        "table": "filter",
        "name": "FORWARD",
        "handle": 6,
        "type": "filter",
        "hook": "forward",
        "prio": 0,
        "policy": "accept"
      }
    },
    {
      "rule": {
        "family": "ip",
        "table": "filter",
        "chain": "FORWARD",
        "handle": 23,
        "expr": [
          {
            "counter": {
              "packets": 12,
              "bytes": 974
            }
          },
          {
            "jump": {
              "target": "DOCKER-USER"
            }
          }
        ]
      }
    },
    {
      "rule": {
        "family": "ip",
        "table": "filter",
        "chain": "FORWARD",
        "handle": 18,
        "expr": [
          {
            "counter": {
              "packets": 12,
              "bytes": 974
            }
          },
          {
            "jump": {
              "target": "DOCKER-ISOLATION-STAGE-1"
            }
          }
        ]
      }
    },
    {
      "rule": {
        "family": "ip",
        "table": "filter",
        "chain": "FORWARD",
        "handle": 17,
        "expr": [
          {
            "match": {
              "op": "==",
              "left": {
                "meta": {
                  "key": "oifname"
                }
              },
              "right": "docker0"
            }
          },
          {
            "xt": None
          },
          {
            "counter": {
              "packets": 6,
              "bytes": 548
            }
          },
          {
            "accept": None
          }
        ]
      }
    },
    {
      "rule": {
        "family": "ip",
        "table": "filter",
        "chain": "FORWARD",
        "handle": 16,
        "expr": [
          {
            "match": {
              "op": "==",
              "left": {
                "meta": {
                  "key": "oifname"
                }
              },
              "right": "docker0"
            }
          },
          {
            "counter": {
              "packets": 0,
              "bytes": 0
            }
          },
          {
            "jump": {
              "target": "DOCKER"
            }
          }
        ]
      }
    },
    {
      "rule": {
        "family": "ip",
        "table": "filter",
        "chain": "FORWARD",
        "handle": 15,
        "expr": [
          {
            "match": {
              "op": "==",
              "left": {
                "meta": {
                  "key": "iifname"
                }
              },
              "right": "docker0"
            }
          },
          {
            "match": {
              "op": "!=",
              "left": {
                "meta": {
                  "key": "oifname"
                }
              },
              "right": "docker0"
            }
          },
          {
            "counter": {
              "packets": 6,
              "bytes": 426
            }
          },
          {
            "accept": None
          }
        ]
      }
    },
    {
      "rule": {
        "family": "ip",
        "table": "filter",
        "chain": "FORWARD",
        "handle": 14,
        "expr": [
          {
            "match": {
              "op": "==",
              "left": {
                "meta": {
                  "key": "iifname"
                }
              },
              "right": "docker0"
            }
          },
          {
            "match": {
              "op": "==",
              "left": {
                "meta": {
                  "key": "oifname"
                }
              },
              "right": "docker0"
            }
          },
          {
            "counter": {
              "packets": 0,
              "bytes": 0
            }
          },
          {
            "accept": None
          }
        ]
      }
    },
    {
      "chain": {
        "family": "ip",
        "table": "filter",
        "name": "DOCKER-USER",
        "handle": 21
      }
    },
    {
      "rule": {
        "family": "ip",
        "table": "filter",
        "chain": "DOCKER-USER",
        "handle": 22,
        "expr": [
          {
            "counter": {
              "packets": 12,
              "bytes": 974
            }
          },
          {
            "return": None
          }
        ]
      }
    }
  ]
}