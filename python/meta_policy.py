import api
import re

class NightlyToProd:
    policies = [
        api.AcceptLink(filters=[
                api.f.state("DEFINED_POLICY"),
                api.f.type("AIN"),
                api.f.endpoint("zone", "nightly", who="client"),
            ], changes=[
                ("client", "zone", "prod"),
            ]),
        api.AcceptLink(filters=[
                api.f.state("DEFINED_POLICY"),
                api.f.type("AEG"),
                api.f.endpoint("zone", "nightly", who="server"),
            ], changes=[
                ("server", "zone", "prod"),
            ]),
    ]
class AcceptAllDefined:
    policies = [
        api.AcceptLink(filters=[
                api.f.state("DEFINED_POLICY"),
            ], changes=[
            ]),
    ]

class MpNAE:
    policies = [
        api.AcceptLink(filters=[
                api.f.type("NAE"),
                api.f.endpoint("process", "/usr/local/bin/cvescan", who="client"),
                api.f.endpoint("dns_pattern", ":people.canonical.com:", who="server"),
            ], changes=[
            ]),
        api.AcceptLink(filters=[
                api.f.type("NAE"),
                api.f.endpoint("process", "grafana-server", who="client"),
                api.f.endpoint("dns_pattern", [
                    ":hooks.slack.com:",
                    ":grafana.com:",
                    ":raw.githubusercontent.com:",
                ], who="server"),
            ], changes=[
            ]),
        api.AcceptLink(filters=[
                api.f.type("NAE"),
                api.f.endpoint("process", "kubelet", who="client"),
                api.f.endpoint("dns_pattern", [
                    ":ec2.us-west-2.amazonaws.com:",
                    ":api.ecr.us-west-2.amazonaws.com:",
                ], who="server"),
            ], changes=[
            ]),
        api.AcceptLink(filters=[
                api.f.type("NAE"),
                api.f.endpoint("process", "kubelet", who="client"),
                api.f.endpoint("dns_pattern", ":.*.eks.amazonaws.com:", who="server"),
            ], changes=[
                ("server", "dns_pattern", ":.*\.eks\.amazonaws\.com:"),
            ]),
        api.AcceptLink(filters=[
                api.f.endpoint("app", "cassandra"),
                api.f.type("NAE"),
                api.f.endpoint("process", "/usr/bin/pip3", who="client"),
                api.f.endpoint("dns_pattern", [":pypi.python.org:",
                                           ":pypi.org:",
                                           ":files.pythonhosted.org:"], who="server"),
            ], changes=[
            ]),
    ]

class MpINT:
    policies = [
        api.AcceptLink(filters=[
                api.f.type("INT"),
                api.f.endpoint("process", "grafana-server", who="client"),
                api.f.endpoint("process", "prometheus", who="server"),
            ], changes=[
            ]),
        api.AcceptLink(filters=[
                api.f.type("INT"),
                api.f.endpoint("process", "kube-rbac-proxy", who="client"),
                api.f.endpoint("process", [
                    "node_exporter",
                    "kube-state-metrics"
                ], who="server"),
            ], changes=[
            ]),
        api.AcceptLink(filters=[
                api.f.type("INT"),
                api.f.endpoint("process", "coredns", who="client"),
                api.f.endpoint("process", "coredns", who="server"),
            ], changes=[
            ]),
        api.AcceptLink(filters=[
                api.f.type("INT"),
                api.f.endpoint("process", "kubelet", who="client"),
                api.f.endpoint("process", "kubelet", who="server"),
            ], changes=[
            ]),
    ]

class MpBendVm:
    policies = [
        api.AcceptLink(filters=[
                api.f.type("NAE"),
                api.f.endpoint("process", "dockerd", who="client"),
                api.f.endpoint("dns_pattern", ":175118736976.dkr.ecr..*.amazonaws.com:", who="server"),
            ], changes=[
                ("server", "dns_pattern", ":175118736976\.dkr\.ecr\..*\.amazonaws\.com:"),
            ]),
        api.AcceptLink(filters=[
                api.f.endpoint("app", "bendvm.bend.web"),
                api.f.type("NAE"),
                api.f.endpoint("process", "araaliweb", who="client"),
                api.f.endpoint("dns_pattern", [":ipinfo.io:", ":metering.marketplace.us-east-1.amazonaws.com:"], who="server"),
            ], changes=[
            ]),
        api.AcceptLink(filters=[
                api.f.endpoint("app", "bend.applens.applens-generator"),
                api.f.type("NAE"),
                api.f.endpoint("process", "com.araalinetworks.LaunchKt", who="client"),
                api.f.endpoint("dns_pattern", [":sns.us-west-2.amazonaws.com:"], who="server"),
            ], changes=[
            ]),
        api.AcceptLink(filters=[
                api.f.endpoint("app", "bendvm.bend.backend"),
                api.f.type("NAE"),
                api.f.endpoint("process", "araali_backend.py", who="client"),
                api.f.endpoint("dns_pattern", [":sns.us-west-2.amazonaws.com:", ":lambda.us-west-2.amazonaws.com:"], who="server"),
            ], changes=[
            ]),
        api.AcceptLink(filters=[
                api.f.endpoint("app", "bendvm.bend.visbot"),
                api.f.type("NAE"),
                api.f.endpoint("process", "main.py", who="client"),
                api.f.endpoint("dns_pattern", [":email.us-west-2.amazonaws.com:", ":slack.com:"], who="server"),
            ], changes=[
            ]),
        api.AcceptLink(filters=[
                api.f.type("INT"),
                api.f.endpoint("process", "araaliweb", who="client"),
                api.f.endpoint("process", "docker-proxy", who="server"),
            ], changes=[
            ]),
        api.AcceptLink(filters=[
                api.f.type("INT"),
                api.f.endpoint("process", "araali_backend.py", who="client"),
                api.f.endpoint("process", "docker-proxy", who="server"),
            ], changes=[
            ]),
        api.AcceptLink(filters=[
                api.f.type("INT"),
                api.f.endpoint("process", "com.araalinetworks.LaunchKt", who="client"),
                api.f.endpoint("process", "scanner.py", who="server"),
            ], changes=[
            ]),
        api.AcceptLink(filters=[
                api.f.endpoint("app", "bendvm"),
                api.f.type("INT"),
                api.f.endpoint("process", "docker-proxy", who="client"),
                api.f.endpoint("process", "main.py", who="server"),
            ], changes=[
            ]),
        api.AcceptLink(filters=[
                api.f.endpoint("app", ".uiserver"),
                api.f.type("INT"),
                api.f.endpoint("process", "grpcwebproxy", who="client"),
                api.f.endpoint("process", "com.araalinetworks.uiserver.UiServerKt", who="server"),
            ], changes=[
            ]),
        api.AcceptLink(filters=[
                api.f.endpoint("app", "bendvm.bend.uiserver"),
                api.f.type("INT"),
                api.f.endpoint("parent_process", "check_health.sh", who="client"),
                api.f.endpoint("process", "grpcwebproxy", who="server"),
            ], changes=[
            ]),
        api.AcceptLink(filters=[
                api.f.endpoint("app", "bendvm.bend.backend"),
                api.f.type("INT"),
                api.f.endpoint("process", "prometheus", who="client"),
                api.f.endpoint("process", "araali_backend.py", who="server"),
            ], changes=[
            ]),
        api.AcceptLink(filters=[
                api.f.same_zone,
                api.f.type("AEG"),
                api.f.endpoint("app", "bendvm.bend.uiserver", who="client"),
                api.f.endpoint("process", "com.araalinetworks.uiserver.UiServerKt", who="client"),
                api.f.endpoint("app", "dmzvm", who="server"),
                api.f.endpoint("process", "haproxy", who="server"),
            ], changes=[
            ]),
        api.AcceptLink(filters=[
                api.f.same_zone,
                api.f.type("AEG"),
                api.f.endpoint("app", "dmzvm", who="client"),
                api.f.endpoint("process", "haproxy", who="client"),
                api.f.endpoint("app", "bendvm.bend.web", who="server"),
                api.f.endpoint("process", "araaliweb", who="server"),
            ], changes=[
            ]),
        api.AcceptLink(filters=[
                api.f.same_zone,
                api.f.type("AEG"),
                api.f.endpoint("app", "dmzvm", who="client"),
                api.f.endpoint("process", "haproxy", who="client"),
                api.f.endpoint("app", "bendvm.bend.uiserver", who="server"),
                api.f.endpoint("process", "grpcwebproxy", who="server"),
            ], changes=[
            ]),
        api.AcceptLink(filters=[
                api.f.same_zone,
                api.f.type("AEG"),
                api.f.endpoint("app", "dmzvm", who="client"),
                api.f.endpoint("process", "haproxy", who="client"),
                api.f.endpoint("app", "bendvm.bend.backend", who="server"),
                api.f.endpoint("process", "araali_backend.py", who="server"),
            ], changes=[
            ]),
    ]

class MpSSMagentToMeta:
    policies = [
        api.AcceptLink(filters=[
                api.f.endpoint("binary_name", "/snap/amazon-ssm-agent/.*/ssm-agent-worker", who="client"),
                api.f.endpoint("subnet", "169.254.169.254", who="server"),
            ], changes=[
                ("client", "binary_name", "/snap/amazon-ssm-agent/[0-9]+/ssm-agent-worker"),
            ]),
    ]

class MpSSMagentToSSM:
    policies = [
        api.AcceptLink(filters=[
                api.f.endpoint("binary_name", "/snap/amazon-ssm-agent/.*/ssm-agent-worker", who="client"),
                api.f.endpoint("dns_pattern", ":ssm.us-west-2.amazonaws.com:", who="server"),
            ], changes=[
                ("client", "binary_name", "/snap/amazon-ssm-agent/[0-9]+/ssm-agent-worker"),
                ("server", "dns_pattern", ":ssm\..*\.amazonaws\.com:"),
            ]),
    ]

class MpCassandra:
    policies = [
        api.AcceptLink(filters=[
                api.f.endpoint("app", "cassandra"),
                api.f.type("INT"),
                api.f.endpoint("process", "org.apache.cassandra.tools.NodeTool", who="client"),
                api.f.endpoint("process", "org.apache.cassandra.service.CassandraDaemon", who="server"),
            ], changes=[
            ]),
        api.AcceptLink(filters=[
                api.f.endpoint("app", "cassandra"),
                api.f.type("INT"),
                api.f.endpoint("process", "curl", who="client"),
                api.f.endpoint("process", "cassandra_monitoring.py", who="server"),
            ], changes=[
            ]),
        api.AcceptLink(filters=[
                api.f.endpoint("process", ["com.araalinetworks.LaunchKt",
                                       "araali_backend.py",
                                       "service_processor.py",
                                       "com.araalinetworks.uiserver.UiServerKt",
                                       "/usr/bin/cqlsh.py",
                                       "sshd"
                                      ], who="client", flags=re.IGNORECASE),
                api.f.endpoint("process", "cassandra", who="server", flags=re.IGNORECASE),
            ], changes=[
            ]),
    ]

class MpDynamo:
    policies = [
        api.AcceptLink(filters=[
                api.f.endpoint("process", ["araali_backend.py",
                                       "com.araalinetworks.uiserver.UiServerKt",
                                       "com.araalinetworks.LaunchKt",
                                       "araaliweb",
                                      ], who="client", flags=re.IGNORECASE),
                api.f.endpoint("dns_pattern", ":dynamodb..*.amazonaws.com:"),
            ], changes=[
                ("server", "dns_pattern", ":dynamodb\..*\.amazonaws\.com:"),
            ]),
    ]

class MpS3:
    policies = [
        api.AcceptLink(filters=[
                api.f.endpoint("process", ["service_processor.py",
                                       "com.araalinetworks.uiserver.UiServerKt",
                                       "com.araalinetworks.LaunchKt",
                                       "araali_backend.py",
                                       "araaliweb",
                                       "/usr/local/bin/aws",
                                      ], who="client", flags=re.IGNORECASE),
                api.f.endpoint("dns_pattern", ":s3\..*\.amazonaws\.com:"),
            ], changes=[
                ("server", "dns_pattern", ":s3\..*\.amazonaws\.com:"),
            ]),
    ]

class MpSnapdToSnapcraft:
    policies = [
        api.AcceptLink(filters=[
                api.f.endpoint("binary_name", "/snap/core/[0-9]+/usr/lib/snapd/snapd", who="client"),
                api.f.endpoint("dns_pattern", ":api.snapcraft.io:"),
            ], changes=[
                ("client", "binary_name", "/snap/core/[0-9]+/usr/lib/snapd/snapd"),
            ]),
    ]

class MpMonitoring:
    policies = [
        api.AcceptLink(filters=[
                api.f.endpoint("app", "^monitoring\."),
                api.f.type("NAE"),
                api.f.endpoint("process", "grafana-server", who="client"),
                api.f.endpoint("dns_pattern", [":stats.grafana.org:",
                                               ":secure.gravatar.com:",
                                              ], who="server"),
            ], changes=[
            ]),
    ]

class MpPerimeter:
    policies = [
        api.AcceptLink(filters=[
                api.f.perimeter,
                api.f.endpoint("zone", ["staging", "mufasa", "rafiki", "prod", "nightly", "dev", "ops", "nightly-k8s"], who="server", flags=re.IGNORECASE),
                api.f.endpoint("app", ["dmzvm", "cassandra", "k8s"], who="server", flags=re.IGNORECASE),
                api.f.endpoint("process", ["sshd", "haproxy"], who="server", flags=re.IGNORECASE),
            ], changes=[
            ]),
        api.AcceptLink(filters=[
                api.f.type(["AEG", "AIN"]),
                api.f.same_zone,
                api.f.endpoint("app", "dmzvm", who="client"),
                api.f.endpoint("process", "sshd", who="client"),
                api.f.endpoint("app", "bendvm", who="server"),
                api.f.endpoint("process", "sshd", who="server"),
            ], changes=[
            ]),
    ]

class MpAmznLinux:
    policies = [
        api.AcceptLink(filters=[
                api.f.endpoint("process", ["/usr/bin/yum", "amazon_linux_extras"], who="client", flags=re.IGNORECASE),
                api.f.endpoint("dns_pattern", ":amazonlinux.us-west-2.amazonaws.com:", who="server", flags=re.IGNORECASE),
            ], changes=[
                ("server", "dns_pattern", ":amazonlinux\..*\.amazonaws\.com:"),
            ]),
    ]

class MpCheckHealth:
    policies = [
        api.AcceptLink(filters=[
                api.f.same_zone,
                api.f.endpoint("parent_process", "check_health.sh", who="client"),
                api.f.endpoint("process", "grpcwebproxy", who="server", flags=re.IGNORECASE),
            ], changes=[
            ]),
    ]

class MpHbCheck:
    policies = [
        api.AcceptLink(filters=[
                api.f.endpoint("binary_name", "/snap/amazon-ssm-agent/.*/ssm-agent-worker", who="client"),
                api.f.endpoint("subnet", "169.254.169.254", who="server"),
            ], changes=[
                ("client", "binary_name", "/snap/amazon-ssm-agent/[0-9]+/ssm-agent-worker"),
            ]),
    ]

    policies = [
        api.AcceptLink(filters=[
                api.f.type("INT"),
                api.f.endpoint("process", "heartbeat_check.py", who="client"),
                api.f.endpoint("process", "com.araalinetworks.LaunchKt", who="server", flags=re.IGNORECASE),
            ], changes=[
            ]),
    ]

class MpHealthCheck:
    policies = [
        api.AcceptLink(filters=[
                api.f.same_zone,
                api.f.endpoint("process", "/var/lib/haproxy/healthcheck.py", who="client"),
                api.f.endpoint("process", "prometheus", who="server", flags=re.IGNORECASE),
            ], changes=[
            ]),
    ]

class MpHaproxyClient:
    policies = [
        api.AcceptLink(filters=[
                api.f.same_zone,
                api.f.endpoint("process", "haproxy", who="client"),
                api.f.endpoint("process", ['araali_backend.py', "grpcwebproxy", "araaliweb", "com.araalinetworks.uiserver.UiServerKt"], who="server", flags=re.IGNORECASE),
            ], changes=[
            ]),
    ]

class MpHaproxyServer:
    policies = [
        api.AcceptLink(filters=[
                api.f.same_zone,
                api.f.endpoint("process", ["com.araalinetworks.uiserver.UiServerKt", "araali_health_check.py"], who="client"),
                api.f.endpoint("process", "haproxy", who="server", flags=re.IGNORECASE),
            ], changes=[
            ]),
    ]

class MpPrometheusAraali:
    policies = [
        api.AcceptLink(filters=[
                api.f.same_zone,
                api.f.endpoint("process", "prometheus", who="client"),
                api.f.endpoint("process", ["araali_backend.py", "com.araalinetworks.LaunchKt"], who="server", flags=re.IGNORECASE),
            ], changes=[
            ]),
    ]

print("Adding meta-policies to runner")
api.mpr.add(
        MpBendVm, MpNAE, MpINT,
        MpSSMagentToMeta,
        MpSSMagentToSSM, MpCassandra, MpDynamo, MpS3,
        MpSnapdToSnapcraft, MpPerimeter,
        MpAmznLinux, MpCheckHealth, MpHbCheck, MpHealthCheck, MpHaproxyClient,
        MpHaproxyServer, MpPrometheusAraali, MpMonitoring,
)
