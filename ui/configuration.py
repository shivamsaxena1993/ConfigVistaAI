
"""
====================================================================
File: configuration.py

Project : ConfigVista AI

Purpose
-------
Phase 1 Standardized Configuration Information Module.

Preserves the existing functionality while presenting the extracted
configuration features in a cleaner, card-based layout ready for
future enhancements.

====================================================================
"""

import streamlit as st


def _feature(label, value):
    st.write(f"{label} : **{value}**")


def _status(label, enabled):
    icon = "✅ Enabled" if enabled else "❌ Disabled"
    st.write(f"{label} : {icon}")


def render_configuration(assessment):
    """Render extracted configuration details."""

    features = assessment["features"]

    st.subheader("Configuration Summary")

    left, right = st.columns(2)

    with left:
        with st.container(border=True):
            st.markdown("#### 🖥️ Device Information")

            _feature("Hostname", features["hostname"])
            _feature("Interfaces", features["interface_count"])
            _feature("VLANs", features["vlan_count"])
            _feature("VRFs", features["vrf_count"])
            _feature("Route Maps", features["route_map_count"])

    with right:
        with st.container(border=True):
            st.markdown("#### 🌐 Routing Protocols")

            _status("BGP", features["has_bgp"])
            _status("OSPF", features["has_ospf"])
            _status("EIGRP", features["has_eigrp"])
            _status("RIP", features["has_rip"])

    st.write("")

    with st.container(border=True):
        st.markdown("#### 🔒 Security & Network Controls")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("ACL Count", features["acl_count"])

        with c2:
            st.metric("Static Routes", features["static_route_count"])

        with c3:
            st.metric("Prefix Lists", features["prefix_list_count"])

    with st.container(border=True):
        st.markdown("#### Future Enhancements")

        st.caption(
            "Reserved for upcoming dissertation phases."
        )

        st.markdown(
            '''
- Vendor Detection
- Device Model Detection
- OS Version Detection
- Interface Classification
- Configuration Complexity Score
- Configuration Health Score
- Topology Awareness
'''
        )

    st.divider()
