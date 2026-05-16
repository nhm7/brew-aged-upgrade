# typed: false
# frozen_string_literal: true

class AgedUpgrade < Formula
  desc "Upgrade Homebrew packages only after they have been outdated for N days"
  homepage "https://github.com/nhm7/homebrew-aged-upgrade"
  url "https://github.com/nhm7/homebrew-aged-upgrade/archive/refs/tags/v1.0.1.tar.gz"
  sha256 "464396fd00b36ba10afe48fb426e5a0a2072ebe56867ea22df2df5c96492b18c"
  version "1.0.1"

  head "https://github.com/nhm7/homebrew-aged-upgrade.git", branch: "main"
  license "MIT"

  depends_on :macos
  uses_from_macos "python3"

  def install
    libexec.install "libexec/brew-aged-upgrade", "libexec/brew-aged-upgrade-core.py"
    bin.write_exec_script libexec/"brew-aged-upgrade"
  end

  test do
    output = shell_output("#{bin}/brew-aged-upgrade help")
    assert_match "start", output
    assert_match "stop", output
    assert_match "status", output
  end
end
