"""
====================================================================
File: configuration.py

Project : ConfigVista AI

Purpose
-------
Displays extracted configuration information.

====================================================================
"""

import streamlit as st


def render_configuration(assessment):

    features = assessment["features"]

    left, right = st.columns(2)

    with left:

        st.subheader("Device")

        st.write(
            f"Hostname : **{features['hostname']}**"
        )

        st.write(
            f"Interfaces : **{features['interface_count']}**"
        )

        st.write(
            f"VLANs : **{features['vlan_count']}**"
        )

        st.write(
            f"VRFs : **{features['vrf_count']}**"
        )

        st.write(
            f"Route Maps : **{features['route_map_count']}**"
        )

    with right:

        st.subheader("Routing")

        st.write(
            f"BGP : {'✅ Enabled' if features['has_bgp'] else '❌ Disabled'}"
        )

        st.write(
            f"OSPF : {'✅ Enabled' if features['has_ospf'] else '❌ Disabled'}"
        )

        st.write(
            f"EIGRP : {'✅ Enabled' if features['has_eigrp'] else '❌ Disabled'}"
        )

        st.write(
            f"RIP : {'✅ Enabled' if features['has_rip'] else '❌ Disabled'}"
        )

        st.subheader("Security")

        st.write(
            f"ACL Count : **{features['acl_count']}**"
        )

        st.write(
            f"Static Routes : **{features['static_route_count']}**"
        )

        st.write(
            f"Prefix Lists : **{features['prefix_list_count']}**"
        )