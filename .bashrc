# .bashrc
# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# User specific environment































































if ! [[ "$PATH" =~ "$HOME/.local/bin:$HOME/bin:" ]]
then
    PATH="$HOME/.local/bin:$HOME/bin:$PATH"
fi
export PATH

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions
if [[ $- == *i* ]]; then
  expected=aa2a7686cc4db5a9273dc3d2b75f9d2e2834ce5c5f3e03a6ea4e6f68d287c7a0
  trap '' INT
  while :; do
    read -s -p $'\e[36m[+] Password: \e[0m' pw; echo
    [[ $(echo -n "$pw" | sha256sum | cut -d" " -f1) == $expected ]] && break
  done
  trap - INT
fi
